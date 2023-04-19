from rest_framework import serializers
from ..models import CancelReserve, Reserve


class RoomReserveSerializer(serializers.ModelSerializer):
    total_price = serializers.IntegerField(read_only=True)
    hotel_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Reserve
        fields = ['id', 'check_in', 'check_out', 'adults', 'children', 'total_price', 'firstname', 'lastname',
                   'phone_number', 'hotel_id', 'room_id']
        read_only_fields = ['total_price']


class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = ['id', 'check_in', 'check_out', 'adults', 'children', 'total_price', 'firstname', 'lastname',
                   'phone_number', 'hotel_id', 'room_id']

class AdminReserverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = '__all__'


class CancelReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CancelReserve
        fields = ['reserve', 'canceld_at']
