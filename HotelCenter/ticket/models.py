from django.db import models
from  Account.models import User
# Create your model
class  TicketForm(models.Model):
    
    class TaskStatus(models.TextChoices):
            PENDING = 'P', 'Pending'
            WAITING = 'W', 'Waiting'
            ASSIGNED = 'A', 'Assigned'
            DONE = 'D', 'Done'
            
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    text =models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    status= models.CharField(max_length=1,default=TaskStatus.PENDING,choices=TaskStatus.choices)
    request  = models.ForeignKey("RequestForm", on_delete=models.CASCADE,related_name="task_list")


class RequestForm(models.Model):
     name=models.CharField(max_length=155)
     