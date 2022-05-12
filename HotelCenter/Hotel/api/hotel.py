import http

# import rest_framework.request
from django.utils.datetime_safe import datetime
from rest_framework import viewsets, permissions, \
    filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.dateparse import parse_date

from ..permissions import *
from ..models import Hotel, Facility, HotelImage, Room, RoomSpace, Reserve, FavoriteHotel
from ..serializers.hotel_serializers import HotelSerializer, FacilitiesSerializer, HotelImgSerializer \
    , FavoriteHotelSerializer
from ..serializers.room_serializers import PublicRoomSerializer
from ..filter_backends import HotelMinRateFilters


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = HotelMinRateFilters
    search_fields = ['city', 'state']

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def create(self, request, *args, **kwargs):
        """
            if current user does not have a hotel already create a hotel
        """
        if Hotel.objects.filter(creator=request.user).count() > 0:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': "Already Have A Hotel."}
                            , content_type='json')
        else:
            request.data
            return super().create(request, *args, **kwargs)

    def filter_size(self, hotels, size: int):

        valid_h = []
        print('\nhotels ', hotels)
        for h in hotels:
            print('\nh in hotels ', h)
            rooms = h.rooms.all()
            print('\n rooms : ', rooms)

            for r in rooms:
                if r.size >= size:
                    valid_h.append(h)
                    break

        return valid_h

    def filter_date(self, hotels, check_in, check_out):
        if check_in >= check_out:
            raise ValueError('not valid dates')
        if check_in < datetime.today().date():
            raise ValueError('not valid dates')

        valid_hotels = set()
        reserves = Reserve.objects.filter(start_day__gte=check_out, end_day__lte=check_in
                                          , roomspace__room__hotel__in=hotels).select_related('roomspace').all()
        spaces = [r.roomspace_id for r in reserves]
        spaces = RoomSpace.objects.filter(room__hotel__in=hotels).exclude(pk__in=spaces).all()
        for s in spaces:
            valid_hotels.add(s.room.hotel)

        return list(valid_hotels)

    def list(self, request, *args, **kwargs):

        query_set = self.filter_queryset(queryset=self.queryset)
        size = 0
        # print('\nquery.size: ', request.query_params.get('size'))
        if request.query_params.get('size'):
            try:
                # print("before cast Size")
                size = int(request.query_params['size'])
                if size < 0:
                    size = 0
                # print('before filter size\n', size)
                query_set = self.filter_size(query_set, size)

            except:
                return Response('Arguments not valid', http.HTTPStatus.BAD_REQUEST)

        if request.query_params.get('check_in'):
            try:
                check_in = parse_date(request.query_params['check_in'])
                check_out = parse_date(request.query_params['check_out'])

                print("check_in", check_in)
                print("check_out", check_out)

                if (check_in is None) or (check_out is None):
                    raise ValueError(message='Not valid date')
                query_set = self.filter_date(query_set, check_in, check_out)
            except:
                return Response('Arguments not valid', http.HTTPStatus.BAD_REQUEST)

        # valid_hotel=[]
        # for hotel in query_set

        return Response(self.serializer_class(query_set, many=True).data, status=http.HTTPStatus.OK)

    # return super(HotelViewSet, self).list(request, *args, **kwargs)


class FacilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitiesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class HotelImgViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin,
                      viewsets.mixins.CreateModelMixin, viewsets.mixins.DestroyModelMixin):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsEditorOrReadOnly]
    serializer_class = HotelImgSerializer

    def get_queryset(self):
        self.queryset = HotelImage.objects.filter(hotel_id=self.h_id).all()
        return self.queryset

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def dispatch(self, request, *args, **kwargs):
        self.request = request

        try:
            self.h_id = int(kwargs.get('hid'))
            self.req_hotel: Hotel = Hotel.objects.get(pk=self.h_id)
        except:
            return Response("hotel not found", status=http.HTTPStatus.NOT_FOUND)

        return super().dispatch(request, *args, **kwargs)

    def create(self, request: rest_framework.request.Request, *args, **kwargs):
        """
        if is_header==true:
            set hotel.header to request.files[image]
        else
            add new image to hotel images
        """

        is_header = request.GET.get("is_header", None)
        if is_header == 'true':
            try:
                # self.req_hotel.header = request.FILES['image']
                img = request.FILES['image']
                # print("in changing header2", self.h_id)
                self.req_hotel = Hotel.objects.get(pk=self.h_id)
                # print("req_hotel", self.req_hotel)
                self.req_hotel.header = img
                self.req_hotel.save()
                # print('change header')
                return Response(HotelSerializer(self.req_hotel).data, 200)
            except:
                print(' in is header error')
                return Response("file not valid", http.HTTPStatus.BAD_REQUEST)

        files = request.data.copy()
        files['hotel'] = self.h_id
        hotelimg = HotelImgSerializer(data=files)
        try:
            hotelimg.is_valid(raise_exception=True)
            hotelimg.save()
            return Response(hotelimg.data, status=http.HTTPStatus.OK)
        except:
            # print('in image', hotelimg)
            return Response("file not valid", http.HTTPStatus.BAD_REQUEST)


class BestHotelViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # queryset = Hotel.objects.order(rate).all()
    serializer_class = HotelSerializer

    def dispatch(self, request: rest_framework.request.Request, *args, **kwargs):
        self.request = request
        self.in_kwargs = kwargs
        self.count = int(request.GET.get('count', 5))

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = Hotel.objects.order_by('-rate').all()[0:self.count]
        return self.queryset


class MyHotelsViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     user = self.request.user
    #     owners = Hotel.objects.filter(owner=user).all()
    #     editors = Hotel.objects.filter(editors__in=[user]).all()
    #
    #     return owners, editors

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super(MyHotelsViewSet, self).dispatch(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        user = request.user
        owners = list(Hotel.objects.filter(creator=user).all())
        editors = list(Hotel.objects.filter(editors__in=[user]).all())
        owners_data = self.serializer_class(instance=owners, many=True)
        editors_data = self.serializer_class(instance=editors, many=True)

        data = {
            "owners": owners_data.data,
            'editors': editors_data.data,
        }
        return Response(data=data, status=http.HTTPStatus.OK)


class HotelSearchViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    """
    search among one hotel rooms
    """

    serializer_class = PublicRoomSerializer

    def get_queryset(self):
        min_size = int(self.request.query_params.get('size', 0))
        # print("\n min size: ", min_size)

        if min_size < 0:
            min_size = 0
        all_rooms = Room.objects.filter(hotel=self.hotel_id, size__gte=min_size).all()

        if self.request.query_params.get('check_in'):
            check_in = parse_date(self.request.query_params['check_in'])
            check_out = parse_date(self.request.query_params['check_out'])

            rooms = self.filter_date(all_rooms, check_in, check_out)
            return rooms

        return all_rooms

    def filter_date(self, rooms, check_in, check_out):

        valid_rooms = []
        for room in rooms:
            spaces = room.spaces.all()

            print('\n\nspaces: ', spaces)
            resv = Reserve.objects.filter(roomspace__in=spaces, start_day__gte=check_out, end_day__lte=check_in).all()
            spa_id = [r.roomspace for r in resv]
            for s in spaces:
                if not (s in spa_id):
                    valid_rooms.append(room)
                    break

        return valid_rooms

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.hotel_id = kwargs['hid']
        self.args = args
        self.kwargs = kwargs

        return super(HotelSearchViewSet, self).dispatch(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if request.query_params.get('check_in'):
            try:
                check_in = parse_date(request.query_params['check_in'])
                check_out = parse_date(request.query_params['check_out'])

            except:
                return Response('Arguments not valid', http.HTTPStatus.BAD_REQUEST)

        if request.query_params.get('size'):
            try:
                size = int(request.query_params['size'])

            except:
                return Response('Arguments not valid', http.HTTPStatus.BAD_REQUEST)

        return super(HotelSearchViewSet, self).list(request, *args, **kwargs)


class FavoriteViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin, viewsets.mixins.CreateModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteHotelSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = FavoriteHotel.objects.filter(user=user)
        return queryset

    def create(self, request: rest_framework.request.Request, *args, **kwargs):
        try:
            hotel_id = int(request.data['hotel_id'])
        except:
            return Response("Field hotel_id required", status=http.HTTPStatus.BAD_REQUEST)

        try:
            hotel = Hotel.objects.get(pk=hotel_id)
        except:
            return Response('Hotel Not found', status=http.HTTPStatus.NOT_FOUND)

        favs: FavoriteHotel = FavoriteHotel.objects.filter(hotel=hotel, user=request.user).first()

        if favs is None:
            new_fav = FavoriteHotel(user=request.user, hotel=hotel)
            new_fav.save()
            nf = FavoriteHotelSerializer(instance=new_fav)

            return Response(nf.data, status=http.HTTPStatus.OK)

        else:
            favs.delete()
            return Response('hotel deleted from favorites', status=http.HTTPStatus.OK)
