from django.shortcuts import render

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from .serializers import TagSerializer,WriteCommentSerializer
from .models import Tag,Comment
from Account.models import User
# Create your views here.

class TagList(ListCreateAPIView):
    queryset=Tag.objects.all()
    serializer_class=TagSerializer
    paginate_by = 5


class Commentdetail(APIView):
    
    serializer_class=WriteCommentSerializer
    
    def post(self,request):
            comment=Comment(writer_id =request.user.id)
            # all_tag=Tag.objects.values_list('id',flat=True)
            # tags=  request.POST.get('tag',[])
            
            # # for i in range(len(tags)):
            #     if i in all_tag:
            #         tag_obj=get_object_or_404(Tag,id=i)
            #         comment.tag.add(tag_obj)
            # if  "tag" in request.data:
                # request.data.pop("tag")
            serializer=WriteCommentSerializer(comment,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response("comment posted!",status=status.HTTP_200_OK)
    
 
        
            
            

