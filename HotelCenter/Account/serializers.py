from rest_framework import serializers
from .models import (User,Manager,Customer)
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer,UserCreatePasswordRetypeSerializer



class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model=User
        fields=['email','phone_number','role','password']
        

        


        
        
  
            
            
            
           

