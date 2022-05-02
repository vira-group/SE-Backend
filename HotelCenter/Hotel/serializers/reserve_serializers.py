from rest_framework import serializers
from ..models import Reserve


class ReserveSerializer(serializers.ModelSerializer):
    total_price = serializers.IntegerField(read_only = True)
    hotel_id = serializers.IntegerField(read_only = True)
    class Meta:
        model = Reserve
        fields = ['id', 'start_day', 'end_day', 'roomspace', 'price_per_day', 'total_price', 'firstname', 'lastname', 'national_code', 'phonen_umber', 'hotel_id', 'user']
        read_only_fields = ['total_price']
