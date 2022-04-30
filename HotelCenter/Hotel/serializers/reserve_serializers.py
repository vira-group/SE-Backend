from rest_framework import serializers
from ..models import Reserve


class ReserveSerializer(serializers.ModelSerializer):
    total_price = serializers.IntegerField()
    class Meta:
        model = Reserve
        fields = ['start_day', 'end_day', 'user', 'roomspace', 'price_per_day', 'total_price']
        read_only_fields = ['roomspace']
