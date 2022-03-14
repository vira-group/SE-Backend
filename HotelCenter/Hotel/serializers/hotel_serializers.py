from rest_framework import serializers
from ..models import Hotel, Facility


class FacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['name']


class HotelSerializer(serializers.ModelSerializer):
    facilities = FacilitiesSerializer(required=False, many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'header', 'city', 'state', 'description', 'facilities', 'rate',
                  'reply_count', 'phone_numbers', 'start_date']
        read_only_fields = ['id', "rate", 'reply_count', 'start_date']
        # lookup_field = 'id'

    def create(self, validated_data):
        request = self.context.get("request")

        # tags = list(request.data.get("tags", []))
        # validated_data["tags"] = []
        #
        # for t in tags:
        #     if Facility.objects.filter(name=t).exist():
        #         validated_data["tags"].append(Facility.objects.get(name=t))

        validated_data['creator'] = request.user
        validated_data['rate'] = 5
        validated_data['reply_count'] = 0
        return super().create(validated_data)
