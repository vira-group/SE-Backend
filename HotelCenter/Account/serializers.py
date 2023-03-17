from rest_framework import serializers
from .models import (User,Manager,Customer)
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer,UserCreatePasswordRetypeSerializer



class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model=User
        fields=['email','phone_number','role','password']
        
        def create(self, validated_data):
            user = User(
            
                
                email=validated_data['email'],
                phone_number=validated_data['phone_number'],
                role=validated_data['role'],

            )
            user.set_password(validated_data['password'])
            user.save()
            
            
            if user.role == "M":
                manager=Manager(user=user,name=f"Manager{user.pk}")
                manager.save()
            elif user.role=="C":
                 customer=Manager(user=user,first_name=f"cutomer{user.pk}",last_name=f"customer_last_name")
                 customer.save()
            else :
                raise ValueError("Value is invalid!")
        
        
            return user
        
 
            



# class ManagerSerializer(serializers.ModelSerializer):
#     role=serializers.CharField(read_only=True)
#     user=UserCreateSerializer()
#     class Meta:
#         model=Manager
#         fields=['user','name']
    
#     def create(self, validated_data):
#         user = User(
           
            
#             email=validated_data['email'],
#             gender=validated_data['gender'],
#             phone_number=validated_data['phone_number'],
#             national_code=validated_data['national_code'],
#             role='M'
#         )
#         user.set_password(validated_data['password'])
#         user.save()
        
#         manager=Manager(
            
#                 user_manager=user,
#                 name=validated_data['name']
#         )
#         manager.save()
        
        
        
#         return manager





# class CutomerSerializer(serializers.ModelSerializer):
#     role=serializers.CharField(read_only=True)
#     user=UserCreateSerializer()
#     class Meta:
#         model=Customer
#         fields=['user','fisrt_name','last_name']
    
#     def create(self, validated_data):
#         user = User(
           
            
#             email=validated_data['email'],
#             gender=validated_data['gender'],
#             phone_number=validated_data['phone_number'],
#             national_code=validated_data['national_code'],
#             role='C'
#         )
#         user.set_password(validated_data['password'])
#         user.save()
        
#         customer=Customer(
            
#                 user_manager=user,
#                 first_name=validated_data['first_name'],
#                 last_name=validated_data['last_name'],
#         )
#         customer.save()
        
        
        
#         return customer
        


        
        
  
            
            
            
           

