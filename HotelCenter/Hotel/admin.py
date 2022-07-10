from django.contrib import admin
from .models import CancelReserve, Hotel, Facility, Room, RoomImage, roomFacility, HotelImage, Reserve,\
                    RoomSpace, FavoriteHotel

admin.site.register(Hotel)
admin.site.register(Facility)
admin.site.register(Room)
admin.site.register(RoomImage)
admin.site.register(roomFacility)
admin.site.register(HotelImage)
admin.site.register(Reserve)
admin.site.register(RoomSpace)
admin.site.register(CancelReserve)
admin.site.register(FavoriteHotel)
