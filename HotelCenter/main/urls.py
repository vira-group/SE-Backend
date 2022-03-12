from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from main.api import userApi
from .api.userApi import publicUserDetail, publicUserList

router = routers.DefaultRouter()
router.register('users', publicUserDetail)
router.register('users', publicUserList)

urlpatterns = [
    path('users/me/', userApi.myProfileDetail),
    path('', include(router.urls)),
]