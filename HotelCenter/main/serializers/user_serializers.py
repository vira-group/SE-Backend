from dataclasses import field
from pyexpat import model
from ..models import User
from rest_framework import serializers
from Hotel.models import Hotel

class PublicUserSerializer(serializers.HyperlinkedModelSerializer):
    avatar = serializers.ImageField(read_only = True)
    firstName = serializers.CharField(read_only = True)
    avatar = serializers.CharField(read_only = True)
    class Meta:
        model = User
        fields = ['avatar','firstName','lastName']

