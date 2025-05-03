"""
mail.py

This module sets up the email configuration for the FastAPI backend using FastAPI-Mail
and provides utility functions to create HTML email messages.
"""

from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import Config
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

# Email server configuration using environment variables from the Config class
mail_config = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,       # Email address used for sending
    MAIL_PASSWORD=Config.MAIL_PASSWORD,       # Email account password or app password
    MAIL_FROM=Config.MAIL_FROM,               # Default "from" address
    MAIL_PORT=Config.MAIL_PORT,               # Port used for SMTP (typically 587 or 465)
    MAIL_SERVER=Config.MAIL_SERVER,           # SMTP server (e.g., smtp.gmail.com)
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,     # Display name of the sender
    MAIL_STARTTLS=True,                       # Use STARTTLS encryption
    MAIL_SSL_TLS=False,                       # Do not use SSL/TLS (conflicts with STARTTLS)
    USE_CREDENTIALS=True,                     # Use credentials for login
    VALIDATE_CERTS=True,                      # Validate SSL certificates
    # TEMPLATE_FOLDER=Path(BASE_DIR, "templates"),  # Uncomment to use templates
)
mail = FastMail(config=mail_config)


def create_message(recipients: list[str], subject: str, body: str):
    """
    Create an HTML email message schema.

    Args:
        recipients (list[str]): List of recipient email addresses.
        subject (str): Subject line of the email.
        body (str): HTML content of the email.

    Returns:
        MessageSchema: A message object that can be sent using FastMail.
    """

    message = MessageSchema(
        recipients=recipients, subject=subject, body=body, subtype=MessageType.html
    )

    return message
