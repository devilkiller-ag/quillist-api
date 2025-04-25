from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.auth.service import UserService
from src.auth.schemas import UserModel, UserCreateModel, UserLoginModel
from src.auth.utils import verify_password, create_access_token
from src.auth.dependencies import RefreshTokenBearer


auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRE_DAYS = 2


@auth_router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=UserModel
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with this email already exists",
        )

    new_user = await user_service.create_user(user_data, session)

    return new_user


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email does not exist",
        )

    password_valid = verify_password(password, user.password_hash)

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid password",
        )

    access_token = create_access_token(
        user_data={"email": user.email, "user_uid": str(user.uid)}
    )

    refresh_token = create_access_token(
        user_data={"email": user.email, "user_uid": str(user.uid)},
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


@auth_router.get("/refresh_token", status_code=status.HTTP_200_OK)
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) < datetime.now():
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token"
        )

    new_access_token = create_access_token(user_data=token_details["user"])

    return JSONResponse({"access_token": new_access_token})
