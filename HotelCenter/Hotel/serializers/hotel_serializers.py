from rest_framework import serializers
from ..models import Hotel, Facility, HotelImage, FavoriteHotel


class FacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['name']


class HotelSerializer(serializers.ModelSerializer):
    facilities = FacilitiesSerializer(required=False, many=True, read_only=True)
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'header', 'city', 'state', 'description', 'facilities', 'rate','is_favorite',
                  'reply_count', 'phone_numbers', 'country', 'check_in_range', "check_out_range", 'start_date',
                  'address', 'capacity']
        read_only_fields = ['id', "rate", 'reply_count', 'start_date', 'capacity']
        # lookup_field = 'id'

    def get_is_favorite(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        else:
            return False

        if user is None:
            return False

        is_fav = FavoriteHotel.objects.filter(user=user.id, hotel=obj.id).exists()

        return is_fav

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
        return cr

    def update(self, instance: Hotel, validated_data):
        request = self.context.get("request")
        if not request.data.get('facilities', None) is None:
            instance.facilities.clear()
            for f in request.data.get('facilities', []):
                if (Facility.objects.filter(name=f['name']).count() > 0):  # and (f not in instance.facilities.all()):
                    instance.facilities.add(Facility.objects.get(pk=f['name']))

            instance.save()
        # print("in hotel update: ", request.data.get('facilities', []))
        return super(HotelSerializer, self).update(instance, validated_data)


class HotelImgSerializer(serializers.ModelSerializer):
    # hotel_name = serializers.RelatedField(source='Hotel.name', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = HotelImage
        fields = ['image', 'id', 'hotel', 'image_url']
        # read_only_fields = ['hotel']

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url


class FavoriteHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteHotel
        fields = ['hotel', 'user_id']


class BestHotelSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['id', 'city', "country", 'header', 'rate', 'reply_count', 'is_favorite', 'name']

    def get_is_favorite(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        else:
            return False

        if user is None:
            return False

        is_fav = FavoriteHotel.objects.filter(user=user.id, hotel=obj.id).exists()

        return is_fav
