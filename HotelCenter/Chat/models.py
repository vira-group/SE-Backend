from django.db import models
from Account.models import User
from Hotel.models import Hotel
class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chat = models.CharField(max_length=100)

    def __str__(self):
        return self.author.id

    def last_10_messages(chat):
        return Message.objects.filter(chat=chat).order_by('timestamp').all()

class HotelChat(models.Model):
    user = models.ForeignKey(User, related_name='hotel_chat_user', on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, related_name='hotel_chat_hotel', on_delete=models.CASCADE)
    roomname = models.CharField(max_length=100)