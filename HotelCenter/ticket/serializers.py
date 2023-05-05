from rest_framework import serializers
from .models import TicketForm,RequestForm
from Account.serializers import PublicUserSerializer



class RequestFormSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    class Meta:
        model=RequestForm
        fields=['id','name']

class TicketFormSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    status=serializers.CharField(read_only=True)
    created_date=serializers.DateTimeField(read_only=True)
    updated_date=serializers.DateTimeField(read_only=True)
    response_text=serializers.CharField(read_only=True)
    class Meta:
        model=TicketForm
        fields=['id','sender','status','text','created_date','request','response_text','updated_date']
    
        
        
class AdminTicketSerializer(serializers.ModelSerializer):
    text=serializers.CharField(max_length=None,read_only=True)
    created_date=serializers.DateTimeField(read_only=True)
    request=RequestFormSerializer(read_only=True)
    sender=PublicUserSerializer(read_only=True)
    class Meta:
        model=TicketForm
        fields=['status','sender','text','created_date','response_text','request']
             
