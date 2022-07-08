from dataclasses import field
from pyexpat import model
from ..models import User
from rest_framework import serializers
from Hotel.models import Hotel


class PublicUserSerializer(serializers.HyperlinkedModelSerializer):
    avatar = serializers.ImageField(read_only=True)
    firstName = serializers.CharField(read_only=True)
    lastName = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['avatar', 'firstName', 'lastName', 'id']


class MyProfileSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'avatar', 'firstName', 'lastName', 'birthday', 'gender', 'phone_number', 'national_code',
                  'balance', 'description']
        read_only_fields = ['balance']


class CreditSerializer(serializers.ModelSerializer):
    credit = serializers.IntegerField(min_value=0)

    class Meta:
        model = User
        fields = ['credit']
