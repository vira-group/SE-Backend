import datetime

from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .serializers.reserve_serializers import ReserveSerializer
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
from celery.utils.log import get_task_logger
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

subject = 'Subject'
html_message = render_to_string('reserve/reserve_reminder.html', {
            'username': "hadi",
            'hotel': "parsian",
            'start_date': "2020-02-03",
            "end_date": "2022-02-05",
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
    # user = kwargs['user']
    username = kwargs['username']
    email = kwargs['email']
    room = kwargs['room']
    size = kwargs['size']
    start_date = kwargs['start_date']
    end_date = kwargs['end_date']
    hotel = kwargs['hotel']

    subject = 'Reminder for your Reservation'

    html_message = render_to_string(template_name, context={
        'username': username,
        'hotel': hotel,
        'start_date': start_date,
        'end_date': end_date,
        'room': room,
        "size": size,
        "hotel_url": "localhost"
    })
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message, fail_silently=True)


# @shared_task
def set_reserve_tasks(Reserve, Reserve_dic=None, **kwargs):
    """
    set before and after reserve tasks
    """
    # room_type = kwargs['room']
    now = datetime.datetime.today() + datetime.timedelta(minutes=20)
    # if now < Reserve.start_day:
    sdt = datetime.datetime.combine(date=Reserve.start_day, time=datetime.time(0, 0))
    rem_date = max(sdt - datetime.timedelta(days=2), now)

    edt = datetime.datetime.combine(date=Reserve.start_day, time=datetime.time(0, 0))
    feedback_date = max(edt + datetime.timedelta(days=1), now)

    user = Reserve.user
    kwargs = {'username': user.username,
              'email': user.email,
              'room': Reserve.room.type,
              'size': Reserve.room.size,
              'start_date': Reserve.start_day,
              'end_date': Reserve.end_day,
              'hotel': Reserve.room.hotel.name}

    pre_reserve.apply_async(args=[Reserve_dic], kwargs=kwargs, eta=rem_date)
    after_reserve.apply_async(args=[Reserve_dic], kwargs=kwargs, eta=feedback_date)

    logger.info("schedule review email")


@shared_task(name="after_reserve")
def after_reserve(Reserve, **kwargs):
    """
    """
    template_name = "reserve/reserve_feedback.html"
    # user = kwargs['user']
    username = kwargs['username']
    email = kwargs['email']

    subject = 'Reminder for your Reservation'
    html_message = render_to_string(template_name, context={

        "hotel_url": "localhost"
    })
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message, fail_silently=True)


@shared_task(name="add_for_test")
def add(a, b):
    logger.info("Sent review email")
    return a, b, a + b
