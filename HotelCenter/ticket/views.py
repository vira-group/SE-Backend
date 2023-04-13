from django.shortcuts import render
from django.shortcuts import get_list_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination 
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .serializers import RequestFormSerializer,ShowTicketSerializer,TicketFormSerializer,AdminTicketSerializer
# Create your views here.