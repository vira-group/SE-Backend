from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.authentication import get_user_model


class Hotel(models.Model):
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="HotelManager")
    name = models.CharField(max_length=70)
    address = models.CharField(max_length=70)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    floor_count = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=55)
    city = models.CharField(max_length=55)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    rate = models.FloatField(validators=[MinValueValidator(
        0.0), MaxValueValidator(5.0)], default=2.5)

    class Meta:
        ordering = ['-rate']

    def __str__(self) -> str:
        return self.name


class roomFacility(models.Model):
    name = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return self.name


def get_upload_path(instance, filename):
    return 'hotel/{0}/{1}'.format(instance.hotel.id, filename)


class HotelImage(models.Model):
    image = models.FileField(null=False, blank=False,
                             upload_to=get_upload_path)
    hotel = models.ForeignKey(
        'Hotel', on_delete=models.CASCADE, related_query_name='images')


class Room(models.Model):
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name='rooms')
    type = models.CharField(max_length=100, null=False,
                            blank=False, default=None)
    size = models.IntegerField(default=0, null=False, blank=False)
    view = models.CharField(max_length=100, null=False,
                            blank=False, default=None)
    capacity = models.IntegerField(default=1, blank=False, null=False)
    price = models.IntegerField(blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    facilities = models.ManyToManyField(roomFacility, related_name='rooms')

    def __str__(self):
        return 'Room of type {} for hotel "{}" '.format(self.type, self.hotel)


class RoomImage(models.Model):
    image = models.ImageField(
        upload_to='test_img/', height_field=None, width_field=None, null=True, blank=True)
    # The room that this image is for
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False)


class Reserve(models.Model):
    check_in = models.DateField()
    check_out = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.DO_NOTHING)
    adults = models.IntegerField(default=None)
    children = models.IntegerField(default=None)
    total_price = models.IntegerField(default=None)
    firstname = models.CharField(max_length=64, blank=False, null=False)
    lastname = models.CharField(max_length=64, blank=False, null=False)
    phone_number = models.CharField(max_length=64, blank=True, null=True)
    room = models.ForeignKey(
        Room, on_delete=models.DO_NOTHING, related_name='reserves')
    create_at = models.DateTimeField(auto_now_add=True)

    @property
    def hotel_id(self):
        room = self.room
        hotel = room.hotel
        return (hotel.id)


class FavoriteHotel(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name='favorites', on_delete=models.CASCADE)
    hotel = models.ForeignKey(
        Hotel, related_name='likes', on_delete=models.CASCADE)

    class Mata:
        unique_together = ('hotel', 'user',)


class CancelReserve(models.Model):
    check_in = models.DateField()
    check_out = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.DO_NOTHING)
    price_per_day = models.IntegerField(default=None)
    firstname = models.CharField(max_length=64, blank=False, null=False)
    lastname = models.CharField(max_length=64, blank=False, null=False)
    national_code = models.CharField(max_length=64, blank=True, null=True)
    phone_number = models.CharField(max_length=64, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
    reserve = models.IntegerField()
    canceld_at = models.DateTimeField(auto_now=True)
