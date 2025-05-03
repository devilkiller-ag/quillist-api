"""
This module contains utility functions for handling user authentication, token creation, and password management.

Key Components:
- generate_password_hash: Generates a hashed version of the provided password using bcrypt.
- verify_password: Verifies if a provided password matches the stored hash.
- create_access_token: Creates a JWT access token with a specified expiry time and optional refresh flag.
- decode_token: Decodes a JWT token and returns its payload.
- create_urlsafe_token: Creates a URL-safe token for secure data exchange, typically for email confirmation.
- decode_urlsafe_token: Decodes a URL-safe token and retrieves its data.
"""

import jwt
import uuid
import logging
from passlib.context import CryptContext
from datetime import timedelta, datetime
from itsdangerous import URLSafeTimedSerializer

from src.config import Config


# Initialize a password context with bcrypt hashing algorithm
password_context = CryptContext(schemes=["bcrypt"])

# Set default expiration time for access tokens to 1 hour (3600 seconds)
ACCESS_TOKEN_EXPIRY = 3600  # 1 hour


def generate_password_hash(password: str) -> str:
    """
    Generates a hashed version of the provided password using bcrypt.

    Args:
        password (str): The plain-text password to be hashed.

    Returns:
        str: The hashed password.
    """

    password_hash = password_context.hash(password)

    return password_hash


def verify_password(password: str, hash: str) -> bool:
    """
    Verifies if the provided password matches the stored hash.

    Args:
        password (str): The plain-text password to verify.
        hash (str): The hashed password stored in the database.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """

    return password_context.verify(password, hash)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
) -> str:
    """
    Creates a JWT access token with a specified expiration time and optional refresh flag.

    Args:
        user_data (dict): A dictionary containing user data to be included in the token payload.
        expiry (timedelta, optional): The expiration time for the token. Defaults to 1 hour if not provided.
        refresh (bool, optional): Flag indicating whether the token is a refresh token. Defaults to False.

    Returns:
        str: The generated JWT access token.
    """

    payload = {}

    payload["user"] = user_data
    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )
    payload["jti"] = str(uuid.uuid4())

    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict:
    """
    Decodes a JWT token and retrieves its payload.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: The decoded token data, or None if the token is invalid or expired.
    """

    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM],
        )

        return token_data

    except jwt.PyJWTError as e:
        logging.exception(e)
        return None


# Initialize a serializer for URL-safe tokens, typically used for email confirmation
serializer = URLSafeTimedSerializer(
    secret_key=Config.JWT_SECRET, salt="email-configuration"
)


def create_urlsafe_token(data: dict) -> str:
    """
    Creates a URL-safe token for secure data exchange, such as email confirmation.

    Args:
        data (dict): The data to be encoded into a URL-safe token.

    Returns:
        str: The generated URL-safe token.
    """

    token = serializer.dumps(data)

    return token


def decode_urlsafe_token(token: str) -> dict:
    """
    Decodes a URL-safe token and retrieves the data encoded in it.

    Args:
        token (str): The URL-safe token to decode.

    Returns:
        dict: The decoded data, or None if the token is invalid or expired.
    """

    try:
        data = serializer.loads(token)

        return data

    except Exception as e:
        logging.exception(e)
        return None
