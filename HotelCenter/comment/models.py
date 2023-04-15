from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from Hotel.models import Hotel


class Comment(models.Model):
    rate = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
        , default=2.5
    )
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="comments")
    hotel = models.ForeignKey(Hotel, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_comment = models.DateTimeField(auto_now_add=True)
    reply=models.OneToOneField("Reply", related_name="comment_reply",on_delete=models.SET_NULL,null=True,blank=True)
    tag=models.ManyToManyField("Tag", related_name="comment_tag",null=True, blank=True) 
    

    class Meta:
        ordering = ['-created_comment']
        
    def __str__(self) -> str:
        return f"text: {self.text}" + " " + f"####### {list(self.tag.all())}"




class Reply(models.Model):
       text_reply=models.TextField()
       created_reply = models.DateTimeField(auto_now_add=True)
       
       class Meta:
         ordering = ['-created_reply']
        





class Tag(models.Model):
    name=models.CharField(max_length=40)
        
    def __str__(self) -> str:
        return  self.name

    
