from rest_framework import serializers
from Hotel.models import Room
from .hotel_serializers import HotelSerializer

class PublicRoomSerializer(serializers.ModelSerializer):
    # hotel = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='name'
    #  )
    hotel_info = serializers.SerializerMethodField()
    class Meta:
        model = Room
        fields = ['hotel','type', 'view', 'sleeps', 'price', 'option', 'hotel_info']
        read_only_fields = ['hotel']
    def get_hotel_info(self, obj):
        hotel = obj.hotel
        serializer = HotelSerializer(hotel)
        data = serializer.data
        return(data)

