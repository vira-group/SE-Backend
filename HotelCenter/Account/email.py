from djoser import email
from djoser import utils
from djoser.conf import settings
from django.contrib.auth.tokens import default_token_generator


 
    # def activation(self, request, uid, token, *args, **kwargs):
    #     super().activation(request, *args, **kwargs)
    #     return Response(status=status.HTTP_204_NO_CONTENT)    


class ActivationEmail(email.ActivationEmail):
    template_name = 'email/emailVerification.html'

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        return context