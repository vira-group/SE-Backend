from rest_framework import serializers
from Hotel.models import Room, roomFacility, RoomImage
from .hotel_serializers import HotelSerializer

class PublicRoomSerializer(serializers.ModelSerializer):
    # hotel = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='name'
    #  )
    
    hotel_info = serializers.SerializerMethodField()
    room_facilities = serializers.SerializerMethodField()
    class Meta:
        model = Room
        fields = ['hotel','type', 'view', 'sleeps', 'price', 'option', 'hotel_info', 'room_facilities']
        read_only_fields = ['hotel']
    def get_hotel_info(self, obj):
        hotel = obj.hotel
        serializer = HotelSerializer(hotel)
        data = serializer.data
        return(data)
    def get_room_facilities(self, obj):
        facility_list = obj.facilities
        serializer = roomFacilitiesSerializer(facility_list, many = True)
        data = serializer.data
        return(data)

class roomFacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = roomFacility
        fields = ['name']

class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['image']