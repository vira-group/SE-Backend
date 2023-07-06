from rest_framework import serializers
from .models import Comment ,Tag,Reply
from Account.serializers import PublicUserSerializer
from django.contrib.auth import get_user_model




class TagSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model=Tag
        fields=['id','name']
        
class SimpleCustomerSerializer(serializers.ModelSerializer):
    
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = get_user_model()
        fields = ['full_name']
        
    def get_full_name (self,obj):
        return obj.first_name + ' ' + obj.last_name
    
class SimpleUserSerializer(serializers.ModelSerializer):
    
    customer=SimpleCustomerSerializer()
    
    class Meta:
        model = get_user_model()
        fields = ['customer']
        
    
        
        
class WriteCommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ['hotel','text','tag','rate']
        
        
        
class ReplySerializer(serializers.ModelSerializer):
    created_reply=serializers.DateTimeField(read_only=True)

    class Meta:
        model=Reply
        fields=['text_reply','created_reply']       


class ReadCommentSerializer(serializers.ModelSerializer):
    tag=TagSerializer(many=True)
    reply=ReplySerializer()
    writer=SimpleUserSerializer()
    class Meta:
        model = Comment
        fields = ['hotel','writer','text','tag','rate','reply','created_comment']




  
       
        

        

