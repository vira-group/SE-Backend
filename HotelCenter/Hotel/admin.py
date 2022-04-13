from django.contrib import admin
from .models import Hotel, Facility, Room, RoomImage

admin.site.register(Hotel)
admin.site.register(Facility)
admin.site.register(Room)
admin.site.register(RoomImage)

