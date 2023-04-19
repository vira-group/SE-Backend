from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from Hotel.models import Hotel


class Comment(models.Model):
    rate = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
        , null=False, blank=False
    )
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="comments")
    hotel = models.ForeignKey(Hotel, related_name='comments', on_delete=models.CASCADE)
    text = models.CharField(max_length=1024, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified_at']
