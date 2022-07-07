import datetime

from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from templated_email import send_templated_mail

"""
send_templated_mail(
        template_name='welcome',
        from_email='from@example.com',
        recipient_list=['to@example.com'],
        context={  # context to be loaded in the template
            'username': "hoi",
            'full_name': "guededag",
            'start_date': "2020-02-03"
        },
    )
    
from django.template.loader import render_to_string
from django.utils.html import strip_tags

subject = 'Subject'
html_message = render_to_string('reserve/reserve_reminder.html', {
            'username': "hadi",
            'hotel': "parsian",
            'start_date': "2020-02-03",
            'room': "room_type",
            "size": "size 45",
            "hotel_url":"localhost"
        })
plain_message = strip_tags(html_message)
from_email = settings.EMAIL_HOST_USER
to = 'dakey43331@shbiso.com'

send_mail(subject, plain_message, from_email, [to], html_message=html_message)
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
    room = Reserve.room.type
    size = Reserve.room.size
    start_date = Reserve.start_day
    hotel = Reserve.room.hotel.name

    subject = 'Reminder for your Reservation'

    html_message = render_to_string(template_name, context={
        'username': username,
        'hotel': hotel,
        'start_date': start_date,
        'room': room,
        "size": size,
        "hotel_url": "localhost"
    })
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)


@shared_task
def set_reserve_tasks(Reserve, **kwargs):
    """
    set before and after reserve tasks
    """

    now = datetime.datetime.now() + datetime.timedelta(minutes=20)
    # if now < Reserve.start_day:
    rem_date = max(Reserve.start_day - datetime.timedelta(days=2), now)

    feedback_date = max(Reserve.end_day + datetime.timedelta(days=1), now)

    pre_reserve.apply_async(args=Reserve, kwargs=kwargs, eta=rem_date)
    after_reserve.apply_async((Reserve, kwargs), eta=feedback_date)

    logger.info("schedule review email")

@shared_task(name="after_reserve")
def after_reserve(Reserve, **kwargs):
    """
    """
    template_name = "reserve/reserve_feedback.html"
    user = Reserve.user
    username = user.username
    email = user.email

    subject = 'Reminder for your Reservation'
    html_message = render_to_string(template_name, context={

        "hotel_url": "localhost"
    })
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)


@shared_task(name="add_for_test")
def add(a, b):
    logger.info("Sent review email")
    return a, b
