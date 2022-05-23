import imp
from django.urls import path
from .api.chat import MessageAPI
urlpatterns = [
    path('messages', MessageAPI.as_view())
]