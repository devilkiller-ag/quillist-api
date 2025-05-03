from typing import Any, Callable
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError


class QuillistException(Exception):
    """Base class for all exceptions raised by Quillist."""

    pass


class InvalidToken(QuillistException):
    """User has provided an invalid or expired token."""

    pass


class RevokeToken(QuillistException):
    """User has provided a token that has been revoked."""

    pass


class AccessTokenRequired(QuillistException):
    """User has provided a refresh token instead of an access token."""

    pass


class RefreshTokenRequired(QuillistException):
    """User has provided an access token instead of a refresh token."""

    pass


class InvalidVerificationToken(QuillistException):
    """User has provided an invalid or expired verification link/token."""

    pass


class UserNotFound(QuillistException):
    """User has provided an email that does not exist in the database."""

    pass


class UserAlreadyExists(QuillistException):
    """User has provided an email during signup that already exists in the database."""

    pass


class InsufficientPermission(QuillistException):
    """User does not have the neccessary permisions to perform an action."""

    pass


class AccountNotVerified(QuillistException):
    """User has not verified their account."""

    pass


class InvalidCredentials(QuillistException):
    """User has provided invalid credentials during login."""

    pass


class ResetPasswordsDoNotMatch(QuillistException):
    """User has provided two different passwords during password reset."""

    pass


class BookNotFound(QuillistException):
    """User has provided a book id that does not exist in the database."""

    pass


class ReviewNotFound(QuillistException):
    """User has provided a review id that does not exist in the database."""

    pass


class TagNotFound(QuillistException):
    """User has provided a tag id that does not exist in the database."""

    pass


class TagAlreadyExists(QuillistException):
    """User has provided a tag that already exists in the database."""

    pass


def create_exception_handler(
    status_code: int,
    initial_detail: Any,
) -> Callable[[Request, Exception], JSONResponse]:
    """Create a custom exception handler for the Quillist API.

    Args:
        status_code (int): The HTTP status code to return.
        initial_detail (Any): The initial detail to include in the response.

    Returns:
        Callable[[Request, Exception], JSONResponse]: A function that takes a request and an exception
            and returns a JSON response with the specified status code and detail.
    """

    async def exception_handler(
        request: Request, exc: QuillistException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content=initial_detail,
        )

    return exception_handler


def register_all_errors(app: FastAPI):
    """Register all custom error handlers for the Quillist API.

    Args:
        app (FastAPI): The FastAPI application instance.
    """

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status.HTTP_401_UNAUTHORIZED,
            {
                "message": "Token is either invalid or has expired",
                "error_code": "invalid_token",
                "resolution": "Please get a new token",
            },
        ),
    )

    app.add_exception_handler(
        RevokeToken,
        create_exception_handler(
            status.HTTP_401_UNAUTHORIZED,
            {
                "message": "Token is either invalid or has been revoked",
                "error_code": "token_revoked",
                "resolution": "Please get a new token",
            },
        ),
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status.HTTP_401_UNAUTHORIZED,
            {
                "message": "Please provide an access token",
                "error_code": "access_token_required",
                "resolution": "Please provide an access token",
            },
        ),
    )

    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status.HTTP_401_UNAUTHORIZED,
            {
                "message": "Please provide a refresh token",
                "error_code": "refresh_token_required",
                "resolution": "Please provide a refresh token",
            },
        ),
    )

    app.add_exception_handler(
        InvalidVerificationToken,
        create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
            {
                "message": "Invalid or expired verification token",
                "error_code": "invalid_verification_token",
                "resolution": "Please check your email for verification details",
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status.HTTP_404_NOT_FOUND,
            {
                "message": "User not found",
                "error_code": "user_not_found",
                "resolution": "Please provide a valid email address",
            },
        ),
    )

    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status.HTTP_409_CONFLICT,
            {
                "message": "User already exists",
                "error_code": "user_already_exists",
                "resolution": "Please provide a different email address",
            },
        ),
    )

    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status.HTTP_403_FORBIDDEN,
            {
                "message": "You do not have the necessary permissions to perform this action",
                "error_code": "insufficient_permissions",
                "resolution": "Please contact support for assistance",
            },
        ),
    )

    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status.HTTP_403_FORBIDDEN,
            {
                "message": "Account not verified",
                "error_code": "account_not_verified",
                "resolution": "Please check your email for verification details",
            },
        ),
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status.HTTP_401_UNAUTHORIZED,
            {
                "message": "Invalid credentials",
                "error_code": "invalid_credentials",
                "resolution": "Please check your email and password",
            },
        ),
    )

    app.add_exception_handler(
        ResetPasswordsDoNotMatch,
        create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
            {
                "message": "Passwords do not match",
                "error_code": "passwords_do_not_match",
                "resolution": "Please ensure both passwords (new password and confirm new password) are the same",
            },
        ),
    )

    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status.HTTP_404_NOT_FOUND,
            {
                "message": "Book not found",
                "error_code": "book_not_found",
                "resolution": "Please provide a valid book ID",
            },
        ),
    )

    app.add_exception_handler(
        ReviewNotFound,
        create_exception_handler(
            status.HTTP_404_NOT_FOUND,
            {
                "message": "Review not found",
                "error_code": "review_not_found",
                "resolution": "Please provide a valid review ID",
            },
        ),
    )

    app.add_exception_handler(
        TagNotFound,
        create_exception_handler(
            status.HTTP_404_NOT_FOUND,
            {
                "message": "Tag not found",
                "error_code": "tag_not_found",
                "resolution": "Please provide a valid tag ID",
            },
        ),
    )

    app.add_exception_handler(
        TagAlreadyExists,
        create_exception_handler(
            status.HTTP_409_CONFLICT,
            {
                "message": "Tag already exists",
                "error_code": "tag_already_exists",
                "resolution": "Please provide a different tag name",
            },
        ),
    )

    async def internal_server_error_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Internal server error",
                "error_code": "internal_server_error",
                "resolution": "Please contact support for assistance",
            },
        )

    app.add_exception_handler(
        status.HTTP_500_INTERNAL_SERVER_ERROR, internal_server_error_handler
    )

    async def database_error_handler(
        request: Request, exc: SQLAlchemyError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Database error",
                "error_code": "database_error",
                "resolution": "Please contact support for assistance",
            },
        )

    app.add_exception_handler(SQLAlchemyError, database_error_handler)
