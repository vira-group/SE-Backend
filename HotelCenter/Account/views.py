from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import User,Manager,Customer
from.serializers import GetRollSerializer,ManagerSerializer,CustomerSerializer,UserShowSerializer
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
class GetRoll(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=get_object_or_404(User,pk=request.user.pk)
        ser=GetRollSerializer(user)
        return Response(ser.data,status=status.HTTP_200_OK)
    
# class GetMyPro(RetrieveUpdateAPIView):
#         permission_classes=[IsAuthenticated]
#         def get_serializer_class(self):
#              if self.request.user.role=="M":
#                  return ManagerSerializer
#              elif self.request.user.role=="C":
#                  return CustomerSerializer
#              else :
#                  return UserShowSerializer
#         def get_queryset(self):
#              if self.request.user.role=="M":
#                  return Manager.objects.all()
#              elif self.request.user.role=="C":
#                  return Customer.objects.all()
#              else :
#                  return User.objects.all()
class GetMyPro(APIView):
    permission_classes=[IsAuthenticated]
    
    def get_serializer_class(self,request):
            if request.user.role=="M":
                 return ManagerSerializer
            elif request.user.role=="C":
                 return CustomerSerializer
            else :
                 return UserShowSerializer
             
    def get_queryset(self,request):
             if request.user.role=="M":
                 return get_object_or_404(Manager,pk=request.user.pk)
             elif request.user.role=="C":
                 return get_object_or_404(Customer,pk=request.user.pk)
             else :
                 return get_object_or_404(User,pk=request.user.pk)

    def get(self,request):
       
          serializer_class=self.get_serializer_class(request)
          user=self.get_queryset(request)
          ser=serializer_class(user)
          return Response(ser.data,status=status.HTTP_200_OK)