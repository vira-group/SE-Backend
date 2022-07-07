from Hotel.serializers import hotel_serializers
from ..models import Message, HotelChat
from rest_framework import serializers
from Account.serializers import user_serializers

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['chat']
        read_only_fields = ['chat']

class HotelChatSerializer(serializers.ModelSerializer):
    user = user_serializers.PublicUserSerializer()
    hotel = hotel_serializers.HotelSerializer()
    class Meta:
        model = HotelChat
        fields = ['user','hotel','roomname']