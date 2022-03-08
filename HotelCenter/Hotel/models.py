from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Facility(models.Model):
    name = models.CharField(unique=True, primary_key=True)

    def __str__(self):
        return self.name


class Hotel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    start_date = models.DateField(auto_created=True)
    description = models.CharField(max_length=1024)
    rate = models.DecimalField(
        max_digits=2, decimal_places=1, default=5, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)])

    reply_count = models.IntegerField()
    check_out_range = models.CharField(max_length=30)  # range of checkout
    check_in_range = models.CharField(max_length=30)  # range of checkout
    facilities = models.ManyToManyField(Facility, related_name="hotels")

    def __str__(self):
        return "%s Hotel" % self.name
