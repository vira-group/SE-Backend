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
from .api.hotel import HotelSearchAPi, NearHotelSearchApi, MyHotelsViewSet, HotelGetInfo, AddNewHotelView, HotelQuery


# from .api.room import RoomList, roomFacilityViewSet, ImageList, RoomSpaceViewSet, AdminRoomSpaceViewSet, \
#     AdminRoomViewSet
# from .api.reserve import ReserveList, RoomspaceReserveList, AdminReserveViewSet, UserCancelReserveList
from .api.room import RoomList, roomFacilityViewSet, ImageList, AdminRoomViewSet
from .api.reserve import MyReservesViewSet, ReserveList, AdminReserveViewSet, UserCancelReserveList

router = routers.DefaultRouter()
router.register('roomfacilities', roomFacilityViewSet,
                basename='roomfacility-list')


hotel_admin_router = routers.DefaultRouter()
hotel_getinfo = routers.DefaultRouter()
hotel_getinfo.register('get_info', HotelGetInfo, basename='get_info')

hotel_router = routers.DefaultRouter()
hotel_router.register('reserves', AdminReserveViewSet,
                      basename='hotel-admin-reserve')
router.register('myhotels', MyHotelsViewSet, basename='my_hotels')
router.register('myreserves', MyReservesViewSet, basename='my_reserves')
hotel_router.register('rooms', AdminRoomViewSet, basename='hotel-admin-room')

room_router = routers.DefaultRouter()
# room_router.register('spaces', RoomSpaceViewSet, basename='room-space')

urlpatterns = [
    path('room/<int:hotel_id>/', RoomList.as_view()),
    path('room/<int:room_id>/images/', ImageList.as_view()),
    path('reserve/room/<int:room_id>/', ReserveList.as_view()),
    # path('reserve', ReserveList.as_view()),
    path('', include(router.urls)),
    path('<int:hid>/', include(hotel_router.urls)),
    path('admin/', include(hotel_admin_router.urls)),
    path('cancelreserve/', UserCancelReserveList.as_view()),
    path('room/<int:room_id>/', include(room_router.urls)),
    # path('create/',HotelCreateListAPi.as_view()),
    path('search/<int:asc>', HotelSearchAPi.as_view()),
    # path('hotelimg/',HotelImgViewSet.as_view()),
    path('nearhotel/', NearHotelSearchApi.as_view(), name="nearhotel"),
    path('', include(hotel_getinfo.urls)),


    path('hotel/', AddNewHotelView.as_view()),
    path('showmyhotel', HotelQuery.as_view({'get': 'show_my_hotels'})),
    path('showmyhotel/deleteimage/<int:id>',
         HotelQuery.as_view({'delete': 'delete_image'})),
    path('deletehotel/<int:id>',
         HotelQuery.as_view({'delete': 'delete_hotel'})),
    # path('updatehotel/<int:id>',HotelQuery.as_view({'patch':'update_note'})),

]
