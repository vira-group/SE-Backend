from rest_framework import serializers
from ..models import Reserve


class RoomReserveSerializer(serializers.ModelSerializer):
    total_price = serializers.IntegerField(read_only=True)
    hotel_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Reserve
        fields = ['id', 'start_day', 'end_day', 'roomspace', 'price_per_day', 'total_price', 'firstname', 'lastname',
                  'national_code', 'phone_number', 'hotel_id', 'user']
        read_only_fields = ['total_price']


class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = ['id', "create_at", 'start_day', 'end_day', 'room', 'price_per_day', 'firstname', 'lastname',
                  'national_code', 'phone_number']


class AdminReserverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = '__all__'
