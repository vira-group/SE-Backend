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
        fields=['phone_number','role','email']
        read_only_fields = ['role', 'email']

class CustomerSerializer(serializers.ModelSerializer):
    user=UserShowSerializer()
    class Meta:
            model=Customer
            fields = ['user','first_name', 'last_name','national_code','gender']
            read_only_fields = ['gender']
            
    def update(self, instance, validated_data):

        user_infos = validated_data.get('user',None)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.national_code = validated_data.get('national_code', instance.national_code)
        instance.save()
      
        if user_infos!=None :
            user_common=User.objects.get(id=instance.user.id)
            # user_common.email=user_infos.get('email',instance.user.email)
            # user_common.phone_number=user_infos.get('phone_number',instance.user.phone_number)
            instance.user.phone_number=user_infos.get('phone_number',instance.user.phone_number)
            # user_common.save()
            
            

        return instance

class ManagerSerializer(serializers.ModelSerializer):
    
    user=UserShowSerializer()
    class Meta:
        model=Manager
        fields=['user','name']
        
    def update(self, instance, validated_data):

        user_infos = validated_data.get('user',None)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
      
        if user_infos!=None :
            user_common=User.objects.get(id=instance.user.id)
            # user_common.email=user_infos.get('email',instance.user.email)
            # user_common.phone_number=user_infos.get('phone_number',instance.user.phone_number)
            instance.user.phone_number=user_infos.get('phone_number',instance.user.phone_number)
            # user_common.save()
            
        return instance




        
        
  
            
            
            
           

