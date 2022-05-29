"""
ASGI config for HotelCenter project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""
import django
django.setup()
# mysite/asgi.py
import os
import channels

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import Chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HotelCenter.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            Chat.routing.websocket_urlpatterns
        )
    ),
})