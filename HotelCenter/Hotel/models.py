from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Facility(models.Model):
    name = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return self.name


class Hotel(models.Model):
    creator = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='hotel', on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=64, blank=False, null=False)  # hotel name showed on profile
    address = models.CharField(max_length=256, blank=False, null=False)
    phone_numbers = models.CharField(max_length=64, blank=True, )
    city = models.CharField(max_length=64, blank=False, null=False)
    state = models.CharField(max_length=64, null=False, blank=True)
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
