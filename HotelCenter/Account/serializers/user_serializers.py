
from ..models import User
from rest_framework import serializers
from ..models import (User,Manager,Customer)




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','gender','phone_number,','national_code','password']




class ManagerSerializer(serializers.ModelSerializer):
    role=serializers.CharField(read_only=True)
    user=UserSerializer()
    class Meta:
        model=Manager
        fields=['user','name']
    
    def create(self, validated_data):
        user = User(
           
            
            email=validated_data['email'],
            gender=validated_data['gender'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            national_code=validated_data['national_code'],
            role='M'
        )
        user.set_password(validated_data['password'])
        user.save()
        
        manager=Manager(
            
                user_manager=user,
                name=validated_data['name']
        )
        manager.save()
        
        
        
        return manager





class CutomerSerializer(serializers.ModelSerializer):
    role=serializers.CharField(read_only=True)
    user=UserSerializer()
    class Meta:
        model=Customer
        fields=['user','fisrt_name','last_name']
    
    def create(self, validated_data):
        user = User(
           
            
            email=validated_data['email'],
            gender=validated_data['gender'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            national_code=validated_data['national_code'],
            role='M'
        )
        user.set_password(validated_data['password'])
        user.save()
        
        customer=Customer(
            
                user_manager=user,
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
        )
        customer.save()
        
        
        
        return customer
        


        
        
  
            
            
            
           

