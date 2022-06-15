from django.conf import settings
from django.core.mail import EmailMessage, get_connection

from celery import shared_task
from celery.utils.log import get_task_logger

from django.core.mail import send_mail, BadHeaderError
from django.conf import settings



logger = get_task_logger(__name__)


@shared_task(name="add_notification")
def add_notification(send_email=False, **kwargs):
    """
        add a notification for the specified user
        in case of send_email == True, notification will be forwarded as an email to the user
    """



