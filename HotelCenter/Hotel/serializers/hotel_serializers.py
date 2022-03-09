from rest_framework import serializers
from HotelCenter.Hotel.models import Hotel, Facility


class FacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['id', 'name']


class HotelSerializer(serializers.ModelSerializer):
    facilities = FacilitiesSerializer(required=False, many=True)

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'city', 'state', 'description', 'facilities', 'rate',
                  'phone_numbers', 'start_date']
        read_only_fields = ["rate", 'reply_count', 'start_date']

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['creator'] = request.user
        validated_data['rate'] = 5
        validated_data['reply_count'] = 0
        return super().create(validated_data)
