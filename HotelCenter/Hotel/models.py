from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator





class Hotel(models.Model):
   manager=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="HotelManager")
   name=models.CharField(max_length=70)
   address=models.CharField(max_length=70)
   phone_number=models.CharField(max_length=11,blank=True,null=True)
   email=models.EmailField(blank=True,null=True)
   description=models.TextField(blank=True,null=True)
   floor_count=models.IntegerField(null=True,blank=True)
   country=models.CharField(max_length=55)
   city=models.CharField(max_length=55)
   longitude=models.FloatField(null=True  , blank=True)
   latitude=models.FloatField(null=True,blank=True)
   check_in=models.TimeField(null=True, blank=True)
   check_out=models.TimeField(null=True, blank=True)
   rate = models.FloatField( validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], default=2.5)

   class Meta:
       ordering = ['-rate']
       
   def __str__(self) -> str:
        return self.name    
   
   
  


class HotelImage(models.Model):
    image = models.ImageField(null=False, blank=False, upload_to='hotel')
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_query_name='images')


# class roomFacility(models.Model):
#     name = models.CharField(max_length=100, unique=True, primary_key=True)

#     def __str__(self):
#         return self.name


# class Room(models.Model):
#     hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')  # The hotel that this room is for
#     type = models.CharField(max_length=100, null=False, blank=False, default=None)
#     size = models.IntegerField(default=0, null=False, blank=False)  # room size(meter)
#     view = models.CharField(max_length=100, null=False, blank=False, default=None)
#     sleeps = models.IntegerField(default=1, blank=False, null=False)  # number of people in the room
#     price = models.IntegerField(blank=False, null=False)
#     option = models.CharField(max_length=100, blank=True, null=True)
#     facilities = models.ManyToManyField(roomFacility, related_name='rooms')

#     def __str__(self):
#         return 'Room of type {} for hotel "{}" '.format(self.type, self.hotel)


# class RoomImage(models.Model):
#     image = models.ImageField(upload_to='roomImages')
#     room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False)  # The room that this image is for


# class RoomSpace(models.Model):
#     name = models.CharField(max_length=100, null=False, blank=False)
#     room = models.ForeignKey(Room, related_name='spaces', on_delete=models.CASCADE)

#     # available = models.BooleanField(default=True)

#     def __str__(self):
#         return f'RoomSpace {self.name} for {self.room}'

#     @property
#     def hotel_id(self):
#         return self.room.hotel.id


# class Reserve(models.Model):
#     start_day = models.DateField()
#     end_day = models.DateField()
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
#     roomspace = models.ForeignKey(RoomSpace, on_delete=models.DO_NOTHING, related_name='reserves')
#     price_per_day = models.IntegerField(default=None)
#     firstname = models.CharField(max_length=64, blank=False, null=False)
#     lastname = models.CharField(max_length=64, blank=False, null=False)
#     national_code = models.CharField(max_length=64, blank=True, null=True)
#     phone_number = models.CharField(max_length=64, blank=True, null=True)
#     room = models.ForeignKey(Room, on_delete=models.DO_NOTHING, related_name='reserves')
#     create_at = models.DateTimeField(auto_now_add=True)

#     @property
#     def total_price(self):
#         total_days = (self.end_day - self.start_day)
#         total_price = (total_days.days + 1) * self.price_per_day
#         return total_price

#     @property
#     def hotel_id(self):
#         room = self.roomspace.room
#         hotel = room.hotel
#         return (hotel.id)


# class FavoriteHotel(models.Model):
#     user = models.ForeignKey(get_user_model(), related_name='favorites', on_delete=models.CASCADE)
#     hotel = models.ForeignKey(Hotel, related_name='likes', on_delete=models.CASCADE)

#     class Mata:
#         unique_together = ('hotel', 'user',)

# class CancelReserve(models.Model):
#     start_day = models.DateField()
#     end_day = models.DateField()
#     user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
#     roomspace = models.ForeignKey(RoomSpace, on_delete=models.DO_NOTHING)
#     price_per_day = models.IntegerField(default=None)
#     firstname = models.CharField(max_length=64, blank=False, null=False)
#     lastname = models.CharField(max_length=64, blank=False, null=False)
#     national_code = models.CharField(max_length=64, blank=True, null=True)
#     phone_number = models.CharField(max_length=64, blank=True, null=True)
#     room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
#     reserve = models.IntegerField()
#     canceld_at = models.DateTimeField(auto_now= True)
