from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import User
from.serializers import GetRollSerializer
from rest_framework import status
class GetRoll(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=get_object_or_404(User,pk=request.user.pk)
        ser=GetRollSerializer(user)
        return Response(ser.data,status=status.HTTP_200_OK)