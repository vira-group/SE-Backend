from django.shortcuts import render
from django.shortcuts import get_list_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination 
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateAPIView
from rest_framework import status
from .serializers import RequestFormSerializer,TicketFormSerializer,AdminTicketSerializer
from .models import RequestForm,TicketForm
# Create your views here.




class TypeRequestsList(ListCreateAPIView): #get list type request and post it 
    serializer_class=RequestFormSerializer
    queryset=RequestForm.objects.all();


class MyTicketList(ListCreateAPIView):   #get list ticket and post it 
    serializer_clas=TicketFormSerializer
    queryset= TicketForm.objects.all()
    
    
class ResponseAdminList(RetrieveUpdateAPIView): ### get one ticket and update it 
    queryset=TicketForm.objects.all()
    serializer_class=AdminTicketSerializer
    