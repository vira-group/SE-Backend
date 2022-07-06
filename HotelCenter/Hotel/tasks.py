from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

from templated_email import send_templated_mail

"""
send_templated_mail(
        template_name='welcome',
        from_email='from@example.com',
        recipient_list=['to@example.com'],
        context={  # context to be loaded in the template
            'username': request.user.username,
            'full_name': request.user.get_full_name(),
            'signup_date': request.user.date_joined
        },
    )
"""

logger = get_task_logger(__name__)


@shared_task(name="pre_reserve")
def pre_reserve(Reserve, **kwargs):
    """
    """
    template_name = "reserve/reserve_reminder.html"
    user = Reserve.user
    username = user.username
    email = user.email

    send_templated_mail(
        template_name=template_name,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        context={
            "start_date": Reserve.start_day,

            "end_date": Reserve.end_day,
            "hotel": Reserve.room.hotel,

            'room': Reserve.room.type,
            # 'hotel_url':,
            'username': username,
        }
    )

@shared_task
def set_reserve_tasks(Reserve,**kwargs):


@shared_task(name="after_reserve")
def after_reserve(Reserve, **kwargs):
    """
    """
    template_name = "reserve/reserve_feedback.html"
    user = Reserve.user
    username = user.username
    email = user.email

    send_templated_mail(
        template_name=template_name,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        context={
            "start_date": Reserve.start_day,

            "end_date": Reserve.end_day,
            "hotel": Reserve.room.hotel,

            'room': Reserve.room.type,
            # 'hotel_url':,
            'username': username,
        }
    )
