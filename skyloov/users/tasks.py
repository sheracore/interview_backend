import random
import logging

from django.conf import settings
from celery import shared_task
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def post_registeration_email(self, recipient, subject, message: str):
    try:
        email = EmailMessage()
        email.subject = subject
        email.body = message
        email.from_email = settings.EMAIL_HOST_USER
        email.to = [recipient]
        email.send()
    except Exception as exc:
        logger.error(f"An error occurred: {exc}")
        raise self.retry(exc=exc, countdown=60 * 60 + random.uniform(1, 60))
