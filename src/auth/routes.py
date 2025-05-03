"""
This module defines routes related to user authentication and account management in the FastAPI application.
It handles user signup, login, email verification, password reset requests, and token refresh functionality.
It also includes email sending functionality and role-based access control.

Routes:
- send_mail: Endpoint to send a welcome email to new users.
- create_user_account: Endpoint to handle user signup, verify email, and send verification email.
- verify_user_account: Endpoint to verify a user's account via a token.
- login_users: Endpoint for user login and JWT token creation (access and refresh tokens).
- get_new_access_token: Endpoint to refresh the access token using a refresh token.
- get_current_user: Endpoint to retrieve the currently authenticated user's data.
- revoke_token: Endpoint to log out a user by blocking their current access token.
- password_reset_request: Endpoint to request a password reset and send a password reset link.
- reset_account_password: Endpoint to confirm password reset after validating the token.
"""

from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, status, BackgroundTasks
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
from src.celery_tasks import send_mail_task


auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])

REFRESH_TOKEN_EXPIRE_DAYS = 2


@auth_router.post("/send-mail")
async def send_mail(emails: EmailModel):
    """
    Sends a welcome email to the provided list of email addresses.

    Args:
        emails (EmailModel): Model containing the email addresses to send the welcome email.

    Returns:
        dict: Confirmation message indicating the email was sent successfully.
    """

    emails = emails.addresses

    subject = "Welcome to Quillist"
    html_message = """
        <h1>Welcome to Quillist</h1>
        <p>Thank you for signing up!</p>
        <p>We are excited to have you on board.</p>
    """

    send_mail_task.delay(
        recipients=emails,
        subject=subject,
        body=html_message,
    )

    return {
        "message": "Email sent successfully",
    }


@auth_router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSignupResponseModel,
)
async def create_user_account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session),
):
    """
    Handles user signup. It creates a new user account, generates a verification token,
    and sends a verification email.

    Args:
        user_data (UserCreateModel): Model containing user signup data.
        session (AsyncSession): Database session dependency.

    Returns:
        dict: A success message and the newly created user details.
    """

    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)

    verification_token = create_urlsafe_token({"email": email})
    verification_link = f"{Config.API_URL}/api/v1/auth/verify/{verification_token}"

    subject = "Verify your Quillist account"
    html_message = f"""
        <h1>Welcome to Quillist</h1>
        <p>Thank you for signing up, {new_user.first_name}!</p>
        <p>Please click <a href="{verification_link}">this</a> link to verify your account.</p>
    """

    send_mail_task.delay(
        recipients=[email],
        subject=subject,
        body=html_message,
    )

    return {
        "message": "Quillist account created! Please check your email to verify your account.",
        "user": new_user,
    }


@auth_router.get("/verify/{token}", status_code=status.HTTP_200_OK)
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):
    """
    Verifies a user's account using the provided token.

    Args:
        token (str): Verification token sent via email.
        session (AsyncSession): Database session dependency.

    Returns:
        JSONResponse: A message indicating whether the account was verified successfully.
    """

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
    """
    Handles user login by validating credentials and generating JWT tokens (access and refresh tokens).

    Args:
        login_data (UserLoginModel): Model containing login credentials (email and password).
        session (AsyncSession): Database session dependency.

    Returns:
        JSONResponse: Login success message along with generated access and refresh tokens.
    """

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
    """
    Refreshes the access token using a valid refresh token.

    Args:
        token_details (dict): Token details extracted from the refresh token.

    Returns:
        JSONResponse: A new access token if the refresh token is valid.
    """

    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) < datetime.now():
        return InvalidToken()

    new_access_token = create_access_token(user_data=token_details["user"])

    return JSONResponse({"access_token": new_access_token})


@auth_router.get("/me", response_model=UserBooksModel)
async def get_current_user(
    user=Depends(get_current_user_dependency), _: bool = Depends(role_checker)
):
    """
    Retrieves the current authenticated user's information.

    Args:
        user (Depends): Dependency to get the current user from the token.
        _: bool: RoleChecker dependency to ensure proper role access.

    Returns:
        UserBooksModel: Current user's data.
    """

    return user


@auth_router.get("/logout")
async def revoke_token(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    """
    Logs out the user by blocking the access token.

    Args:
        token_details (dict): Token details extracted from the access token.
        session (AsyncSession): Database session dependency.

    Returns:
        JSONResponse: A message indicating successful logout.
    """

    jti = token_details["jti"]

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={"message": "Logged out successfully"}, status_code=status.HTTP_200_OK
    )


@auth_router.post("/password-reset-request")
async def password_reset_request(email_data: PasswordResetRequestModel):
    """
    Sends a password reset request email with a link to reset the password.

    Args:
        email_data (PasswordResetRequestModel): Model containing the email address for password reset.

    Returns:
        JSONResponse: A message confirming that the password reset link was sent.
    """

    email = email_data.email

    pasword_rest_link_token = create_urlsafe_token({"email": email})
    pasword_rest_link = (
        f"{Config.API_URL}/api/v1/auth/password-reset-confirm/{pasword_rest_link_token}"
    )

    subject = "Reset your Quillist account password"
    html_message = f"""
        <h1>Reset your Quillist account password!</h1>
        <p>Please click <a href="{pasword_rest_link}">this</a> link to reset your account password.</p>
    """

    send_mail_task.delay(
        recipients=[email],
        subject=subject,
        body=html_message,
    )

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
    """
    Resets the user's password after confirming the token and validating the new password.

    Args:
        token (str): Password reset token sent via email.
        passwords (PasswordResetConfirmModel): Model containing the new password and its confirmation.
        session (AsyncSession): Database session dependency.

    Returns:
        JSONResponse: A message indicating that the password has been successfully reset.
    """

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
