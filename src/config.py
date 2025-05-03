"""
Configuration module for the Quillist FastAPI application.

This module uses `pydantic-settings` to load environment-specific settings
from a `.env` file into a strongly-typed Settings class. It also configures
Celery's Redis broker and result backend for background task processing.

Environment variables required in `.env`:
- DATABASE_URL
- REDIS_URL
- JWT_SECRET
- JWT_ALGORITHM
- MAIL_USERNAME
- MAIL_PASSWORD
- MAIL_SERVER
- MAIL_PORT
- MAIL_FROM
- API_URL
- MAIL_FROM_NAME
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration settings using Pydantic's BaseSettings.

    These settings are loaded from environment variables defined in a `.env` file,
    with some default values provided.
    """

    API_URL: str = "http://localhost:8000"
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_URL: str = "redis://localhost:6379/0"
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.google.com"
    MAIL_FROM_NAME: str = "Quillist"
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = True
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    # Settings model config for environment loading
    model_config = SettingsConfigDict(
        env_file=".env",  # Load variables from a .env file
        extra="ignore",  # Ignore undefined extra variables in the env file
    )


# Instantiate the settings object to access configuration throughout the application
Config = Settings()


# Redis settings used by Celery for background task queue and results storage
broker_url = Config.REDIS_URL
result_backend = Config.REDIS_URL
