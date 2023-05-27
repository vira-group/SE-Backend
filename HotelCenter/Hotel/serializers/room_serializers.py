import datetime

from rest_framework import serializers
from ..models import Room, roomFacility, RoomImage, Reserve
from .hotel_serializers import HotelSerializer


class PublicRoomSerializer(serializers.ModelSerializer):

    hotel_info = serializers.SerializerMethodField()
    room_facilities = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['hotel_info','hotel', 'type', 'size', 'view', 'capacity', 'price', 'description', 'room_facilities', 'id']
        read_only_fields = ['hotel']

    def get_hotel_info(self, obj):
        hotel = obj.hotel
        serializer = HotelSerializer(hotel)
        data = serializer.data
        return (data)

    def get_room_facilities(self, obj):
        facility_list = obj.facilities
        serializer = roomFacilitiesSerializer(facility_list, many=True)
        data = serializer.data
        return data


class roomFacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = roomFacility
        fields = ['name']


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['image']
    def update(self, instance, validated_data):
        instance.image = validated_data['image']
        instance.save()
        return instance



# class AdminRoomSpaceSerializer(serializers.ModelSerializer):
#     room_type = serializers.SerializerMethodField()
#     status = serializers.SerializerMethodField()

#     class Meta:
#         model = RoomSpace
#         fields = ['room', 'name', 'id', 'room_type', 'status']
#         read_only_fields = ['room', 'id', 'room_type']

#     def get_room_type(self, obj):
#         if obj.room:
#             return obj.room.type

#     def get_status(self, obj):
#         date = datetime.date.today()
#         c = Reserve.objects.filter(check_in__lte=date, check_out__gte=date, roomspace=obj).count()
#         if c > 0:
#             return 'reserved'
#         else:
#             return 'available'