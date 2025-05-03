"""
Celery task module for background job processing.

This module initializes a Celery app instance and defines background tasks
used in the Quillist backend, such as sending emails asynchronously.
"""

from celery import Celery
from asgiref.sync import async_to_sync

from src.mail import mail, create_message


celery_app = Celery()

celery_app.config_from_object("src.config")


@celery_app.task()
def send_mail_task(recipients: list[str], subject: str, body: str):
    message = create_message(
        recipients=recipients,
        subject=subject,
        body=body,
    )
    """
    Celery task to send an email asynchronously.

    Args:
        recipients (list[str]): List of recipient email addresses.
        subject (str): Subject line of the email.
        body (str): Plain-text or HTML content of the email body.

    This task is executed by a Celery worker in the background and uses the
    FastAPI-Mail integration to construct and send the email.

    Notes:
        Since `mail.send_message` is an asynchronous function, we use
        `async_to_sync` to call it within a synchronous Celery task.
    """

    async_to_sync(mail.send_message)(message)

    print(f"Email with subject '{subject}' sent to recipients: {recipients}")
