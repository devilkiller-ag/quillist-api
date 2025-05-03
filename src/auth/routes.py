from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.db.redis import add_jti_to_blocklist
from src.auth.service import UserService
from src.auth.utils import (
    verify_password,
    create_access_token,
    create_urlsafe_token,
    decode_urlsafe_token,
    generate_password_hash,
)
from src.auth.schemas import (
    EmailModel,
    UserBooksModel,
    UserLoginModel,
    UserCreateModel,
    UserSignupResponseModel,
    PasswordResetRequestModel,
    PasswordResetConfirmModel,
)
from src.auth.dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user as get_current_user_dependency,
    RoleChecker,
)
from src.config import Config
from src.mail import mail, create_message
from src.errors import (
    UserNotFound,
    InvalidToken,
    UserAlreadyExists,
    InvalidCredentials,
    InvalidVerificationToken,
    ResetPasswordsDoNotMatch,
)


auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])

REFRESH_TOKEN_EXPIRE_DAYS = 2


@auth_router.post("/send-mail")
async def send_mail(emails: EmailModel):
    emails = emails.addresses

    html = """
        <h1>Welcome to Quillist</h1>
        <p>Thank you for signing up!</p>
        <p>We are excited to have you on board.</p>
    """

    message = create_message(
        recipients=emails,
        subject="Welcome to Quillist",
        body=html,
    )

    await mail.send_message(message)

    return {
        "message": "Email sent successfully",
    }


@auth_router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSignupResponseModel,
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)

    verification_token = create_urlsafe_token({"email": email})
    verification_link = (
        f"http://{Config.DOMAIN}/api/v1/auth/verify/{verification_token}"
    )
    html_message = f"""
        <h1>Welcome to Quillist</h1>
        <p>Thank you for signing up, {new_user.first_name}!</p>
        <p>Please click <a href="{verification_link}">this</a> link to verify your account.</p>
    """
    message = create_message(
        recipients=[email],
        subject="Verify your Quillist account",
        body=html_message,
    )

    await mail.send_message(message)

    return {
        "message": "Quillist account created! Please check your email to verify your account.",
        "user": new_user,
    }


@auth_router.get("/verify/{token}", status_code=status.HTTP_200_OK)
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):
    try:
        decoded_token = decode_urlsafe_token(token)
    except Exception as e:
        return InvalidVerificationToken()

    email = decoded_token.get("email")

    if not email:
        return InvalidVerificationToken()

    user = await user_service.get_user_by_email(email, session)

    if not user:
        return UserNotFound()

    await user_service.update_user(user, {"is_verified": True}, session)

    return JSONResponse(
        content={"message": "Account verified successfully! You can now log in."},
        status_code=status.HTTP_200_OK,
    )


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is None:
        raise UserNotFound()

    password_valid = verify_password(password, user.password_hash)

    if not password_valid:
        raise InvalidCredentials()

    access_token = create_access_token(
        user_data={"email": user.email, "user_uid": str(user.uid), "role": user.role},
    )

    refresh_token = create_access_token(
        user_data={"email": user.email, "user_uid": str(user.uid), "role": user.role},
        expiry=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        refresh=True,
    )

    return JSONResponse(
        content={
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "uid": str(user.uid),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        }
    )


@auth_router.get("/refresh-token", status_code=status.HTTP_200_OK)
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) < datetime.now():
        return InvalidToken()

    new_access_token = create_access_token(user_data=token_details["user"])

    return JSONResponse({"access_token": new_access_token})


@auth_router.get("/me", response_model=UserBooksModel)
async def get_current_user(
    user=Depends(get_current_user_dependency), _: bool = Depends(role_checker)
):
    return user


@auth_router.get("/logout")
async def revoke_token(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    jti = token_details["jti"]

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={"message": "Logged out successfully"}, status_code=status.HTTP_200_OK
    )


@auth_router.post("/password-reset-request")
async def password_reset_request(email_data: PasswordResetRequestModel):
    email = email_data.email

    pasword_rest_link_token = create_urlsafe_token({"email": email})
    pasword_rest_link = f"http://{Config.DOMAIN}/api/v1/auth/password-reset-confirm/{pasword_rest_link_token}"
    html_message = f"""
        <h1>Reset your Quillist account password!</h1>
        <p>Please click <a href="{pasword_rest_link}">this</a> link to reset your account password.</p>
    """
    message = create_message(
        recipients=[email],
        subject="Reset your Quillist account password",
        body=html_message,
    )

    await mail.send_message(message)

    return JSONResponse(
        content={
            "message": "Password reset link sent! Please check your email to reset your password."
        },
        status_code=status.HTTP_200_OK,
    )


@auth_router.post("/password-reset-confirm/{token}", status_code=status.HTTP_200_OK)
async def reset_account_password(
    token: str,
    passwords: PasswordResetConfirmModel,
    session: AsyncSession = Depends(get_session),
):
    if passwords.new_password != passwords.confirm_new_password:
        return ResetPasswordsDoNotMatch()

    try:
        decoded_token = decode_urlsafe_token(token)
    except Exception as e:
        return InvalidVerificationToken()

    email = decoded_token.get("email")

    if not email:
        return InvalidVerificationToken()

    user = await user_service.get_user_by_email(email, session)

    if not user:
        return UserNotFound()

    new_password_hash = generate_password_hash(passwords.new_password)

    await user_service.update_user(user, {"password_hash": new_password_hash}, session)

    return JSONResponse(
        content={"message": "Password reset successfully! You can now log in."},
        status_code=status.HTTP_200_OK,
    )
