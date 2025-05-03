"""
This module contains dependencies related to authentication and authorization for the FastAPI application.
It includes functionality for verifying and validating tokens, extracting the current authenticated user,
and checking the user's role for access control.

Key Components:
- TokenBearer: Base class for token validation with logic for checking token validity, expiration, and blocklist status.
- AccessTokenBearer: Inherits TokenBearer, specifically used for validating access tokens.
- RefreshTokenBearer: Inherits TokenBearer, specifically used for validating refresh tokens.
- get_current_user: A FastAPI dependency to extract the current user based on the access token.
- RoleChecker: A callable class that ensures the current user has the necessary role to access a route.
"""

from typing import List
from fastapi import Request, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import User
from src.db.main import get_session
from src.db.redis import token_in_blocklist
from src.auth.utils import decode_token
from src.auth.service import UserService
from src.errors import (
    InvalidToken,
    AccountNotVerified,
    AccessTokenRequired,
    RefreshTokenRequired,
    InsufficientPermission,
)

user_service = UserService()


class TokenBearer(HTTPBearer):
    """
    TokenBearer is a base class for handling token-based authentication.
    It is responsible for:
    - Extracting the token from the request's authorization header.
    - Verifying if the token is valid and not in the blocklist.
    - Ensuring that the token data meets the required conditions (to be implemented in child classes).
    """

    def __init__(self, auto_error=True):
        """
        Initialize the TokenBearer class.

        Args:
            auto_error (bool): Whether to raise an error automatically when token validation fails. Defaults to True.
        """

        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        """
        Extract and validate the token from the request.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            dict: Decoded token data if the token is valid.

        Raises:
            InvalidToken: If the token is invalid or in the blocklist.
        """

        creds = await super().__call__(request)

        token = creds.credentials

        if not self.token_valid(token):
            raise InvalidToken()

        token_data = decode_token(token)

        if await token_in_blocklist(token_data["jti"]):
            raise InvalidToken()

        self.verify_token_data(token_data)

        return token_data

    def token_valid(self, token: str) -> bool:
        """
        Validates the token by attempting to decode it.

        Args:
            token (str): The token to validate.

        Returns:
            bool: True if the token is valid (decoded successfully), False otherwise.
        """

        token_data = decode_token(token)

        return True if token_data is not None else False

    def verify_token_data(self, token_data: dict) -> None:
        """
        Verifies the decoded token data.

        This method must be overridden by subclasses to implement specific token validation logic.

        Args:
            token_data (dict): The decoded token data.

        Raises:
            NotImplementedError: This method should be overridden in child classes.
        """

        raise NotImplementedError("Please Override this method in child classes")


class AccessTokenBearer(TokenBearer):
    """
    AccessTokenBearer is used specifically for verifying access tokens.
    It ensures that the token is not a refresh token.
    """

    def verify_token_data(self, token_data: dict) -> None:
        """
        Verifies the token data to ensure it's an access token (not a refresh token).

        Args:
            token_data (dict): The decoded token data.

        Raises:
            AccessTokenRequired: If the token is a refresh token instead of an access token.
        """

        if token_data and token_data["refresh"]:
            raise AccessTokenRequired()


class RefreshTokenBearer(TokenBearer):
    """
    RefreshTokenBearer is used specifically for verifying refresh tokens.
    It ensures that the token is a refresh token (not an access token).
    """

    def verify_token_data(self, token_data: dict) -> None:
        """
        Verifies the token data to ensure it's a refresh token (not an access token).

        Args:
            token_data (dict): The decoded token data.

        Raises:
            RefreshTokenRequired: If the token is not a refresh token.
        """

        if token_data and not token_data["refresh"]:
            raise RefreshTokenRequired()


async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    """
    Retrieves the current authenticated user based on the provided access token.

    Args:
        token_details (dict): The decoded token data, injected by AccessTokenBearer.
        session (AsyncSession): The database session for querying user data.

    Returns:
        User: The User object corresponding to the email in the token.
    """

    user_email = token_details["user"]["email"]

    user = await user_service.get_user_by_email(user_email, session)

    return user


class RoleChecker:
    """
    RoleChecker is used to check if the current user has one of the allowed roles
    to access a route. This ensures that only users with the required permissions can access certain routes.
    """

    def __init__(self, allowed_roles: List[str]):
        """
        Initializes the RoleChecker with the allowed roles.

        Args:
            allowed_roles (List[str]): A list of roles that are allowed to access the route.
        """

        self.allowed_roles = allowed_roles

    def __call__(self, current_user=Depends(get_current_user)):
        """
        Verifies if the current user has the necessary role to access the route.

        Args:
            current_user (User): The current user, injected by get_current_user.

        Returns:
            bool: True if the user has an allowed role, False otherwise.

        Raises:
            AccountNotVerified: If the user's account is not verified.
            InsufficientPermission: If the user does not have an allowed role.
        """

        if not current_user.is_verified:
            raise AccountNotVerified()

        if current_user.role in self.allowed_roles:
            return True

        raise InsufficientPermission()
