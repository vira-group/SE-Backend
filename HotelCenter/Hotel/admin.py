from django.contrib import admin
from .models import Hotel, Facility, Room, RoomImage, roomFacility

admin.site.register(Hotel)
admin.site.register(Facility)
admin.site.register(Room)
admin.site.register(RoomImage)
admin.site.register(roomFacility)

