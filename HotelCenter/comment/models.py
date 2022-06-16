from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from ..Hotel.models import Hotel


class Comment(models.Model):
    rate = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
        , null=False, blank=False
    )
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="comments")
    hotel = models.ForeignKey(Hotel, related_name='comments')
    text = models.CharField(max_length=1024, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['hotel', 'writer'], ]
