from rest_framework import serializers
from .models import Comment ,Tag,Reply
from Account.serializers import PublicUserSerializer







class TagSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model=Tag
        fields=['id','name']
        
class WriteCommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ['hotel','text','tag','rate']
        
        
        
class ReplySerializer(serializers.ModelSerializer):
    created_reply=serializers.DateTimeField(read_only=True)

    class Meta:
        model=Reply
        fields=['text_reply','created_reply'] 
        # read_only_fields=['comment_reply']       


class ReadCommentSerializer(serializers.ModelSerializer):
    tag=TagSerializer(many=True)
    reply=ReplySerializer()
    class Meta:
        model = Comment
        fields = ['hotel','text','tag','rate','reply']




  
       
        

        

