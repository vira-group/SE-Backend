from ..models import User
from ..serializers.user_serializers import PublicUserSerializer
from rest_framework import generics
from rest_framework import viewsets


class publicUserList(viewsets.ViewSet, generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = PublicUserSerializer

class publicUserDetail(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = PublicUserSerializer
