import random
import logging
# from skyloov.utilities.email import send_email
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def post_registeration_email(self, message: str):
    try:
        print("I executed")
        # send_email(message)
    except Exception as exc:
        logger.error(f"An error occurred: {exc}")
        raise self.retry(exc=exc, countdown=60 * 60 + random.uniform(1, 60))
