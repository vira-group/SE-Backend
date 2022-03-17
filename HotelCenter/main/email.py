from djoser.conf import settings
from djoser import utils, email
from django.contrib.auth.tokens import default_token_generator
from templated_mail.mail import BaseEmailMessage


class ActivationEmail(email.ActivationEmail):
    template_name = "email/emailVerification.html"


