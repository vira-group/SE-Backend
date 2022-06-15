# for mor information check the following URL:
# https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#django-first-steps

from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HotelCenter.settings')

app = Celery('HotelCenter')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
