# from django.contrib import admin
from django.urls import path, include
from .views import GetRoll,GetMyPro
# from rest_framework import routers
# from Account.api import userApi
# from .api.creditApi import CreditViewSet
# # from .api.userApi import publicUserDetail, publicUserList

# # router = routers.DefaultRouter()
# # router.register('users', publicUserDetail)
# # router.register('users', publicUserList)
# # router.register('credit', CreditViewSet, basename='add_credit')

urlpatterns = [
    path('getroll/', GetRoll.as_view()),
    path('profile/', GetMyPro.as_view(),name="profile"),
    # path('', include(router.urls)),

]
