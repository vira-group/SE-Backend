from django.conf import settings
from django.core.mail import EmailMessage, get_connection

from celery import shared_task


