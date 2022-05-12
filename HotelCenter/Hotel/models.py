from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from Account.models import User
from rest_framework.authentication import get_user_model


class Facility(models.Model):
    name = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return self.name


class Hotel(models.Model):
    creator = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='hotel', on_delete=models.CASCADE, null=False)
    editors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="editable_hotels")
    name = models.CharField(max_length=64, blank=False, null=False)  # hotel name showed on profile
    address = models.CharField(max_length=256, blank=False, null=False)
    header = models.ImageField(null=True, blank=True)
    phone_numbers = models.CharField(max_length=64, blank=True, )
    city = models.CharField(max_length=64, blank=False, null=False)
    state = models.CharField(max_length=64, null=False, blank=True)
    country = models.CharField(max_length=64, null=False, blank=True)
    type = models.CharField(max_length=64, default='Hotel', null=False, blank=False)
    start_date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=1024, default="desc")
    rate = models.DecimalField(
        max_digits=2, decimal_places=1, default=5, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)])

    reply_count = models.IntegerField(default=0, )
    check_out_range = models.CharField(max_length=30)  # range of checkout
    check_in_range = models.CharField(max_length=30)  # range of checkout
    facilities = models.ManyToManyField(Facility, related_name="hotels")

    def __str__(self):
        return "%s Hotel, from %s" % (self.name, self.city)

    @property
    def image_url(self):
        try:
            img = self.header.url
        except:
            img = ''
        return img


class HotelImage(models.Model):
    image = models.ImageField(null=False, blank=False, upload_to='hotel')
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_query_name='images')


class roomFacility(models.Model):
    name = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')  # The hotel that this room is for
    type = models.CharField(max_length=100, null=False, blank=False, default=None)
    size = models.IntegerField(default=0, null=False, blank=False)
    view = models.CharField(max_length=100, null=False, blank=False, default=None)
    sleeps = models.IntegerField(default=1, blank=False, null=False)
    price = models.IntegerField(blank=False, null=False)
    option = models.CharField(max_length=100, blank=True, null=True)
    facilities = models.ManyToManyField(roomFacility, related_name='rooms')

    def __str__(self):
        return 'Room of type {} for hotel "{}" '.format(self.type, self.hotel)


class RoomImage(models.Model):
    image = models.ImageField(upload_to='roomImages')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False)  # The room taht this image is for


class RoomSpace(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    room = models.ForeignKey(Room, related_name='spaces', on_delete=models.CASCADE)

    # available = models.BooleanField(default=True)

    def __str__(self):
        return f'RoomSpace {self.name} for {self.room}'

    @property
    def hotel_id(self):
        return self.room.hotel.id


class Reserve(models.Model):
    start_day = models.DateField()
    end_day = models.DateField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    roomspace = models.ForeignKey(RoomSpace, on_delete=models.DO_NOTHING, related_name='reserves')
    price_per_day = models.IntegerField(default=None)
    firstname = models.CharField(max_length=64, blank=False, null=False)
    lastname = models.CharField(max_length=64, blank=False, null=False)
    national_code = models.CharField(max_length=64, blank=True, null=True)
    phone_number = models.CharField(max_length=64, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)

    @property
    def total_price(self):
        total_days = (self.end_day - self.start_day)
        total_price = (total_days.days + 1) * self.price_per_day
        return total_price

    @property
    def hotel_id(self):
        room = self.roomspace.room
        hotel = room.hotel
        return (hotel.id)


class FavoriteHotel(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='favorites', on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, related_name='likes', on_delete=models.CASCADE)
