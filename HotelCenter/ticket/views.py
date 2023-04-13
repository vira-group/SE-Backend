from django.shortcuts import render
from django.shortcuts import get_list_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination 
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from .serializers import RequestFormSerializer,TicketFormSerializer,AdminTicketSerializer
from .models import RequestForm,TicketForm
# Create your views here.




class TypeRequestsList(ListCreateAPIView):
    serializer_class=RequestFormSerializer
    queryset=RequestForm.objects.all();


class MyTicketList(ListCreateAPIView):
    serializer_clas=TicketFormSerializer
    queryset= TicketForm.objects.all()