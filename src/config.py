from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DOMAIN: str = "localhost:8000"
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
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

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


Config = Settings()
