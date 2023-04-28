from rest_framework import serializers
from .models import (User,Manager,Customer)
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer,UserCreatePasswordRetypeSerializer



class UserCreateSerializer(BaseUserCreateSerializer):
    password = serializers.CharField(write_only=True)
    class Meta(BaseUserCreateSerializer.Meta):
        model=User
        fields=['email','phone_number','role','password']
        
class PublicUserSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(read_only=True)
    lastName = serializers.CharField(read_only=True)

    class Meta:
        model = Customer
        fields = ['firstName', 'lastName']
        
class GetRollSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role']
        
        
class UserShowSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','role','phone_number','balance','is_active']

class CustomerSerializer(serializers.ModelSerializer):
    user=UserShowSerializer()
    class Meta:
            model=Customer
            fields = ['user','first_name', 'last_name','national_code','gender']

class ManagerSerializer(serializers.ModelSerializer):
    
    user=UserShowSerializer()
    class Meta:
        model=Manager
        fields=['user','name']



        
        
  
            
            
            
           

