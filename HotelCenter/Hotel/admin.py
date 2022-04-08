from django.contrib import admin
from .models import Hotel, Facility
from Hotel.models import Room
from Hotel.models import RoomImage

admin.site.register(Hotel)
admin.site.register(Facility)
admin.site.register(Room)
admin.site.register(RoomImage)

