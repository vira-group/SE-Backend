from django.urls import  path, include
from rest_framework import routers
from .api.chat import UserChatList, HotelChatAPI

from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('mychatlist/', UserChatList.as_view()),
    path('hotelcaht/<int:hotel_id>', HotelChatAPI.as_view()),
    path('<str:room_name>/', views.room, name='room'),
]