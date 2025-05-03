"""
This module contains Pydantic models used for user authentication and account management in the FastAPI application.
These models handle data validation and serialization for user-related operations such as signup, login,
user details retrieval, and password reset.

Schemas:
- UserModel: Represents a user entity with basic information like username, email, and verification status.
- UserSignupResponseModel: Response model for user signup, including a message and user details.
- UserBooksModel: Extends UserModel to include related books and reviews for a user.
- UserCreateModel: Request model for creating a new user account, including validation for username, email, and password.
- UserLoginModel: Request model for user login, validating email and password.
- EmailModel: Model for handling email addresses, typically for sending emails to multiple recipients.
- PasswordResetRequestModel: Model for requesting a password reset using the user's email address.
- PasswordResetConfirmModel: Model for confirming a password reset with new password fields and validation.

The models utilize Pydantic's BaseModel for data validation and serialization, ensuring input data is valid and properly structured.
"""

import uuid
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field

from src.books.schemas import Book
from src.reviews.schemas import ReviewModel


class UserModel(BaseModel):
    """
    Represents a user entity with essential information.

    Attributes:
        uid (uuid.UUID): Unique identifier for the user.
        username (str): The username of the user.
        email (str): The user's email address.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        is_verified (bool): Indicates whether the user's email is verified.
        password_hash (str): The hashed password, excluded from serialization.
        created_at (datetime): Timestamp of when the user was created.
        updated_at (datetime): Timestamp of the user's last update.
    """

    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime


class UserSignupResponseModel(BaseModel):
    """
    Response model for user signup, includes a success message and the user details.

    Attributes:
        message (str): A message indicating the result of the signup operation.
        user (UserModel): The user object containing user details.
    """

    message: str
    user: UserModel


class UserBooksModel(UserModel):
    """
    Extends UserModel to include information about books and reviews associated with the user.

    Attributes:
        books (List[Book]): A list of books that the user has in their collection or has created.
        reviews (List[ReviewModel]): A list of reviews written by the user.
    """

    books: List[Book]
    reviews: List[ReviewModel]


class UserCreateModel(BaseModel):
    """
    Request model for creating a new user account. It validates the required fields during user signup.

    Attributes:
        username (str): The username chosen by the user. Max length of 12 characters.
        email (str): The email address for the user. Max length of 50 characters.
        password (str): The password for the account. Minimum length of 6 characters.
        first_name (str): The user's first name. Max length of 25 characters.
        last_name (str): The user's last name. Max length of 25 characters.
    """

    username: str = Field(max_length=12)
    email: str = Field(max_length=50)
    password: str = Field(min_length=6)
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)


class UserLoginModel(BaseModel):
    """
    Request model for user login, validating the provided email and password.

    Attributes:
        email (str): The user's email address for login. Max length of 50 characters.
        password (str): The user's password for authentication. Minimum length of 6 characters.
    """

    email: str = Field(max_length=50)
    password: str = Field(min_length=6)


class EmailModel(BaseModel):
    """
    Model for handling email addresses, typically used for sending emails to multiple recipients.

    Attributes:
        addresses (List[str]): A list of email addresses.
    """

    addresses: List[str]


class PasswordResetRequestModel(BaseModel):
    """
    Model for requesting a password reset using the user's email.

    Attributes:
        email (str): The email address associated with the user's account for password reset.
    """

    email: str


class PasswordResetConfirmModel(BaseModel):
    """
    Model for confirming a password reset. It validates the new password and its confirmation.

    Attributes:
        new_password (str): The new password to set. Minimum length of 6 characters.
        confirm_new_password (str): The confirmation of the new password. Must match `new_password`.
    """

    new_password: str = Field(min_length=6)
    confirm_new_password: str = Field(min_length=6)
