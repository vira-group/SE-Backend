from rest_framework import serializers
from .models import TicketForm,RequestForm
from Account.serializers import PublicUserSerializer



class RequestFormSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    class Meta:
        Model=RequestForm
        fields=['id','name']

class TicketFormSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    sender=PublicUserSerializer()
    status=serializers.CharField(read_only=True)
    created_date=serializers.DateTimeField(read_only=True)
    class Meta:
        Model=TicketForm
        fields=['id','sender','status','text','created_date','request']
    
        
        
class AdminTicketSerializer(serializers.ModelSerializer):
    text=serializers.CharField(max_length=None,read_only=True)
    created_date=serializers.DateTimeField(read_only=True)
    request=RequestFormSerializer(read_only=True)
    class Meta:
        Model=TicketForm
        fields=['status','text','created_date','response_text','requset']
        
        
class ShowTicketSerializer(serializers.ModelSerializer):
    sender=PublicUserSerializer(read_only=True)
    request=RequestFormSerializer(read_only=True)
    
    class Meta:
        Model=TicketForm
        fields=['sender','status','text','created_date','response_text','requset','updated_date']
        read_only='__all__'

        
        

