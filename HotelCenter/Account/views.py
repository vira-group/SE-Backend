from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import User,Manager,Customer
from.serializers import GetRollSerializer,ManagerSerializer,CustomerSerializer,UserSerializer
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
class GetRoll(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=get_object_or_404(User,pk=request.user.pk)
        ser=GetRollSerializer(user)
        return Response(ser.data,status=status.HTTP_200_OK)
    
class GetMyPro(RetrieveUpdateAPIView):
        permission_classes=[IsAuthenticated]
        def get_serializer_class(self):
             if self.request.user.role=="M":
                 return ManagerSerializer
             elif self.request.user.role=="C":
                 return CustomerSerializer
             else :
                 return UserSerializer
        def get_queryset(self):
             if self.request.user.role=="M":
                 return Manager.objects.all()
             elif self.request.user.role=="C":
                 return Customer.objects.all()
             else :
                 return User.objects.all()