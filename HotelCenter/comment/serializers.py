from rest_framework import serializers
from .models import Comment ,Tag,Reply
from Account.serializers import PublicUserSerializer







class TagSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model=Tag
        fields=['name']
        
class WriteCommentSerializer(serializers.ModelSerializer):
    
    tag=TagSerializer(Many=True)
    class Meta:
        model = Comment
        fields = ['writer','text','tag']
        
        
        
class ReplySerializer(serializers.ModelSerializer):
    created_reply=serializers.DateTimeField(read_only=True)

    class Meta:
        model=Reply
        fields=['comment_reply','text_reply','created_reply'] 
        read_only_fields=['comment_reply']       





  
       
        

        

