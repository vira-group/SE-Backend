from django.conf import settings
from django.core.mail import EmailMessage, get_connection

from celery import shared_task
from celery.utils.log import get_task_logger

from django.core.mail import send_mail, BadHeaderError
from django.conf import settings



logger = get_task_logger(__name__)


@shared_task(name="pre_reserve")
def pre_reserve(Reserve, **kwargs):
    """
    """

@shared_task(name="after_reserve")
def after_reserve(Reserve, **kwargs):
    """
    """



