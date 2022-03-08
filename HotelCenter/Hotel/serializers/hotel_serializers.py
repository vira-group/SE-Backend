from rest_framework import serializers
from HotelCenter.Hotel.models import Hotel, Facility


class HotelSerializer(serializers.ModelSerializerSerializer):

    class Meta:
        class Meta:
            model = Hotel
            fields = [] #****
            read_only_fields = []
