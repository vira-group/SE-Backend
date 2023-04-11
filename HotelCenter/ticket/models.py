from django.db import models
from  Account.models import User
# Create your model
class  TicketForm(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    text =models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    