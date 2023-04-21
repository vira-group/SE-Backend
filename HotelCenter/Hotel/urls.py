"""Hotel URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .api.hotel import HotelCreateListAPi,HotelSearchAPi,NearHotelSearchApi,MyHotels
# from .api.room import RoomList, roomFacilityViewSet, ImageList, RoomSpaceViewSet, AdminRoomSpaceViewSet, \
#     AdminRoomViewSet
# from .api.reserve import ReserveList, RoomspaceReserveList, AdminReserveViewSet, UserCancelReserveList
from .api.room import RoomList, roomFacilityViewSet, ImageList, AdminRoomViewSet
from .api.reserve import ReserveList, AdminReserveViewSet, UserCancelReserveList

router = routers.DefaultRouter()
router.register('roomfacilities', roomFacilityViewSet, basename='roomfacility-list')


hotel_admin_router = routers.DefaultRouter()


hotel_router = routers.DefaultRouter()
hotel_router.register('reserves', AdminReserveViewSet, basename='hotel-admin-reserve')
# hotel_router.register('roomspaces', AdminRoomSpaceViewSet, basename='hotel-admin-roomspace')
hotel_router.register('rooms', AdminRoomViewSet, basename='hotel-admin-room')

room_router = routers.DefaultRouter()
# room_router.register('spaces', RoomSpaceViewSet, basename='room-space')

urlpatterns = [
    path('room/<int:hotel_id>/', RoomList.as_view()),
    path('room/<int:room_id>/images/', ImageList.as_view()),
    path('reserve/room/<int:room_id>/', ReserveList.as_view()),
    #path('reserve', ReserveList.as_view()),
    path('', include(router.urls)),
    path('<int:hid>/', include(hotel_router.urls)),
    path('admin/', include(hotel_admin_router.urls)),
    path('cancelreserve/', UserCancelReserveList.as_view()),
    path('room/<int:room_id>/', include(room_router.urls)),
    path('create/',HotelCreateListAPi.as_view()),
    path('search/',HotelSearchAPi.as_view()),
    path('nearhotel/',NearHotelSearchApi.as_view()),
    path('myhotels/', MyHotels.as_view()),

]