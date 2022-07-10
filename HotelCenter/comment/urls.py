from django.urls import path, include
from rest_framework import routers
from .api.comment import UserHotelCommentViewSet, HotelCommentViewSet

router = routers.DefaultRouter()
router.register('comments', HotelCommentViewSet, basename="hotel-comment")
router.register('mycomment', UserHotelCommentViewSet, basename="hotel-mycomment")

urlpatterns = [
    path('<int:hid>/', include(router.urls))
]
