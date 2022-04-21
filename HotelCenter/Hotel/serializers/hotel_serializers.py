from rest_framework import serializers
from ..models import Hotel, Facility, HotelImage


class FacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['name']


class HotelSerializer(serializers.ModelSerializer):
    facilities = FacilitiesSerializer(required=False, many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'header', 'city', 'state', 'description', 'facilities', 'rate',
                  'reply_count', 'phone_numbers', 'start_date', 'address']
        read_only_fields = ['id', "rate", 'reply_count', 'start_date']
        # lookup_field = 'id'

    def create(self, validated_data):
        request = self.context.get("request")
        # validated_data["facilities"] = []

        validated_data['creator'] = request.user
        validated_data['rate'] = 5
        validated_data['reply_count'] = 0

        validated_data['header'] = request.FILES.get('header')
        cr: Hotel = super().create(validated_data)
        # print('in hotel serializer\nNew hotel: ', cr)
        for f in request.data.get('facilities', []):
            if Facility.objects.filter(name=f['name']).count() > 0:
                cr.facilities.add(Facility.objects.get(pk=f['name']))

        cr.save()
        # print('in hotel serializer\nNew hotel with facility: ', cr)

        return cr


class HotelImgSerializer(serializers.ModelSerializer):
    # hotel_name = serializers.RelatedField(source='Hotel.name', read_only=True)

    class Meta:
        model = HotelImage
        fields = ['image', 'id', 'hotel']
        # read_only_fields = ['hotel']
