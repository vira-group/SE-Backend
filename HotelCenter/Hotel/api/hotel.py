import http

# import rest_framework.request
from django.utils.datetime_safe import datetime
from rest_framework import viewsets, permissions, \
    filters, status
from datetime import timedelta
from rest_framework.viewsets import ModelViewSet
from dateutil.relativedelta import relativedelta
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.dateparse import parse_date
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from ..permissions import *
from ..models import Hotel, HotelImage, Reserve
from rest_framework.pagination import PageNumberPagination
from ..serializers.hotel_serializers import HotelSerializer, HotelImgSerializer, HotelSearchSerializer,HotelFullInfoSerializer
# from ..serializers.room_serializers import
# from ..filter_backends import HotelMinRateFilters
from ..serializers.hotel_serializers import HotelSerializer
from django.db.models import F, Q
from math import sqrt, pow
from rest_framework.decorators import action
from django .db.models.query import QuerySet

from rest_framework.permissions import IsAuthenticated, AllowAny
from HotelCenter.permissions import IsManager

class HotelPagination(PageNumberPagination):
    page_size = 3

class HotelGetInfo(ModelViewSet):
    queryset=Hotel.objects.all()
    serializer_class=HotelFullInfoSerializer
    permission_class=[AllowAny]
    pagination_class=HotelPagination
    http_method_names=['get']

# class HotelCreateListAPi(ListCreateAPIView):

#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly]

#     serializer_class = HotelSerializer
#     queryset = Hotel.objects.all()
class AddNewHotelView(APIView):
    serializer_class = HotelSerializer

    def post(self, request, *args, **kwargs):
        notepost = Hotel.objects.create(manager_id=request.user.id)
        hotel_serializer = HotelSerializer(notepost, data=self.request.data)
        hotel_serializer.is_valid(raise_exception=True)
        _hotel = hotel_serializer.save()
        print(self.request.data)
        for file in self.request.FILES.getlist('files'):
            print(file)
            print(_hotel)
            hotel_files = HotelImgSerializer(

                data={
                    'image': file,
                    'hotel': _hotel.id

                }
            )
            hotel_files.is_valid(raise_exception=True)
            hotel_files.save()
        return Response(status=status.HTTP_200_OK)


class HotelQuery(ModelViewSet):
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()

    pagination_class = PageNumberPagination

    @action(detail=False, methods=['GET'])
    def show_my_hotels(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 4
        queryset = paginator.paginate_queryset(
            Hotel.objects.filter(manager_id=request.user.id), request)
        serializer = HotelSerializer(queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, method=['DELETE'])
    def delete_image(self, request, id):
        getimage = get_object_or_404(
            HotelImage, id=id, hotel__manager_id=request.user.id)
        getimage.delete()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, method=['DELETE'])
    def delete_hotel(self, request, id):
        gethotel = get_object_or_404(Hotel, id=id, manager_id=request.user.id)
        gethotel.delete()
        return Response(status=status.HTTP_200_OK)


class HotelSearchAPi(APIView):

    permission_classes = [AllowAny]

    def get(self, request, asc, *args, **kwargs):
        city = request.GET.get('city', '')
        check_in = request.GET.get('check_in', '1990-1-01')
        check_out = request.GET.get('check_out', '1990-12-01')
        size = request.GET.get('size', None)

        queryset = None

        field = ""
        if asc != 0:
            field = "price"
        else:
            field = "-price"

        if size == None:
            # queryset=Room.objects.filter(hotel__city__icontains=city,size__gte=1).prefetch_related('reserves').all()
            # ids_room=list(Room.objects.filter(room__size__gte=1,room__hotel__city__icontains=city).values_list('id',flat=True))
            # queryset=Reserve.objects.filter(~(Q(check_in__gte=check_in) & Q(check_out__lte=check_out))).filter(room__size__gte=1,room__hotel__city__icontains=city)
            # queryset2=Reserve.objects.select_related("reserves").get()
            result = []
            queryset = Room.objects.filter(Q(capacity__gte=1) & Q(hotel__city__icontains=city) & ~(
                Q(reserves__check_in__gte=check_in) & Q(reserves__check_out__lte=check_out))).order_by(field)
            # for i in list(queryset):
            #     if len(list(i.reserves))==0:
            #         result.append(i)

        else:
            #  queryset=Room.objects.filter(hotel__city__icontains=city,size=size)
            queryset = Room.objects.filter(Q(capacity=size) & Q(hotel__city__icontains=city) & ~(
                Q(reserves__check_in__gte=check_in) & Q(reserves__check_out__lte=check_out))).order_by(field)

        ser = HotelSearchSerializer(queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class NearHotelSearchApi(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        x = request.GET.get('x', 0)
        y = request.GET.get('y', 0)
        radius = 1
        queryset = Hotel.objects.all()
        li_queryset = list(queryset)
        result = []
        for h in li_queryset:
            cal = sqrt(pow((float(x)-h.latitude), 2) +
                       pow((float(y)-h.longitude), 2))

            # print(cal,h.id)

            if cal <= radius:
                result.append(h)
        ser = HotelSerializer(result, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class HotelViewSet(viewsets.ModelViewSet):

    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    # filterset_class = HotelMinRateFilters
    search_fields = ['city']

    # def get_serializer_context(self):
    #     """
    #     Extra context provided to the serializer class.
    #     """
    #     return {
    #         'request': self.request,
    #         'format': self.format_kwarg,
    #         'view': self
    #     }

    def create(self, request, *args, **kwargs):
        """
            if current user does not have a hotel already create a hotel
        """
        if Hotel.objects.filter(manager=request.user).count() > 0:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': "Already Have A Hotel."}, content_type='json')
        else:
            return super().create(request, *args, **kwargs)

    def filter_size(self, hotels, size: int):

        valid_h = []

        for h in hotels:

            rooms = h.rooms.all()
            for r in rooms:
                if r.sleeps >= size:
                    valid_h.append(h)
                    break

        return valid_h

    def filter_date(self, hotels, check_in, check_out):
        if check_in >= check_out:
            raise ValueError('not valid dates')
        if check_in < datetime.today().date():
            raise ValueError('not valid dates')

        valid_hotels = set()
        reserves = Reserve.objects.filter(start_day__gte=check_out, end_day__lte=check_in,
                                          roomspace__room__hotel__in=hotels).select_related('roomspace').all()
        spaces = [r.roomspace_id for r in reserves]
        # spaces = RoomSpace.objects.filter(room__hotel__in=hotels).exclude(pk__in=spaces).all()
        for s in spaces:
            valid_hotels.add(s.room.hotel)

        return list(valid_hotels)

    def list(self, request, *args, **kwargs):

        query_set = self.filter_queryset(queryset=self.queryset)
        size = 0
        if request.query_params.get('size'):
            try:
                size = int(request.query_params['size'])
                if size < 0:
                    size = 0
                query_set = self.filter_size(query_set, size)

            except:
                return Response('Arguments not valid', http.HTTPStatus.BAD_REQUEST)

        if request.query_params.get('check_in'):
            try:
                check_in = parse_date(request.query_params['check_in'])
                check_out = parse_date(request.query_params['check_out'])

                if (check_in is None) or (check_out is None):
                    raise ValueError(message='Not valid date')
                query_set = self.filter_date(query_set, check_in, check_out)
            except:
                return Response('Arguments not valid', http.HTTPStatus.BAD_REQUEST)

        return Response(self.serializer_class(query_set, many=True, context=self.get_serializer_context()).data,
                        status=http.HTTPStatus.OK)
        # valid_hotel=[]
        # for hotel in query_set

    # return super(HotelViewSet, self).list(request, *args, **kwargs)


# class FacilityViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Facility.objects.all()
#     serializer_class = FacilitiesSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# class BestHotelViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     # queryset = Hotel.objects.order(rate).all()
#     serializer_class = BestHotelSerializer

#     def dispatch(self, request: rest_framework.request.Request, *args, **kwargs):
#         self.request = request
#         self.in_kwargs = kwargs
#         try:
#             self.count = int(request.GET.get('count', 4))
#         except:
#             self.count = 4

#         return super().dispatch(request, *args, **kwargs)

#     def get_queryset(self):
#         self.queryset = Hotel.objects.order_by('-rate').all()[0:self.count]
#         return self.queryset


class MyHotelsViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super(MyHotelsViewSet, self).dispatch(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        user = request.user
        managers = list(Hotel.objects.filter(manager=user).all())
        # editors = list(Hotel.objects.filter(editors__in=[user]).all())
        managers_data = self.serializer_class(instance=managers, many=True)
        # editors_data = self.serializer_class(instance=editors, many=True)

        data = {
            'managers': managers_data.data,
        }
        return Response(data=data, status=http.HTTPStatus.OK)


# class HotelSearchViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
#     """
#     search among one hotel rooms
#     """

#     serializer_class = PublicRoomSerializer

    # def get_queryset(self):
    #     min_size = int(self.request.query_params.get('size', 1))
    #     # print("\n min size: ", min_size)

    #     if min_size < 1:
    #         min_size = 1
    #     all_rooms = Room.objects.filter(hotel=self.hotel_id, sleeps__gte=min_size).all()

    #     if self.request.query_params.get('check_in'):
    #         check_in = parse_date(self.request.query_params['check_in'])
    #         check_out = parse_date(self.request.query_params['check_out'])

    #         rooms = self.filter_date(all_rooms, check_in, check_out)
    #         return rooms

    #     return all_rooms

    # def filter_date(self, rooms, check_in, check_out):

    #     valid_rooms = []
    #     for room in rooms:
    #         spaces = room.spaces.all()

    #         # print('\n\nspaces: ', spaces)
    #         resv = Reserve.objects.filter(roomspace__in=spaces, start_day__gte=check_out, end_day__lte=check_in).all()
    #         spa_id = [r.roomspace for r in resv]
    #         for s in spaces:
    #             if not (s in spa_id):
    #                 valid_rooms.append(room)
    #                 break

    #     return valid_rooms

#     def dispatch(self, request, *args, **kwargs):
#         self.request = request
#         self.hotel_id = kwargs['hid']
#         self.args = args
#         self.kwargs = kwargs

#         return super(HotelSearchViewSet, self).dispatch(request, *args, **kwargs)

#     def list(self, request, *args, **kwargs):
#         if request.query_params.get('check_in'):
#             try:
#                 check_in = parse_date(request.query_params['check_in'])
#                 check_out = parse_date(request.query_params['check_out'])

#             except:
#                 return Response('Arguments not valid', http.HTTPStatus.BAD_REQUEST)

#         if request.query_params.get('size'):
#             try:
#                 size = int(request.query_params['size'])

#             except:
#                 return Response('Arguments not valid', http.HTTPStatus.BAD_REQUEST)

#         return super(HotelSearchViewSet, self).list(request, *args, **kwargs)


# class FavoriteViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin, viewsets.mixins.CreateModelMixin):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = FavoriteHotelSerializer

#     def get_queryset(self):
#         user = self.request.user
#         queryset = FavoriteHotel.objects.filter(user=user).all()
#         return queryset

#     def create(self, request: rest_framework.request.Request, *args, **kwargs):
#         try:
#             hotel_id = int(request.data['hotel_id'])
#         except:
#             return Response("Field hotel_id required", status=http.HTTPStatus.BAD_REQUEST)

#         try:
#             hotel = Hotel.objects.get(pk=hotel_id)
#         except:
#             return Response('Hotel Not found', status=http.HTTPStatus.NOT_FOUND)

#         favs: FavoriteHotel = FavoriteHotel.objects.filter(hotel=hotel, user=request.user).first()

#         if favs is None:
#             new_fav = FavoriteHotel(user=request.user, hotel=hotel)
#             new_fav.save()
#             nf = FavoriteHotelSerializer(instance=new_fav, context=self.get_serializer_context())

#             return Response(nf.data, status=http.HTTPStatus.OK)

#         else:
#             favs.delete()
#             return Response('hotel deleted from favorites', status=http.HTTPStatus.OK)


# class HotelInfoViewSet(viewsets.GenericViewSet, viewsets.mixins.RetrieveModelMixin):
#     permission_classes = (IsEditor, permissions.IsAuthenticated)
#     queryset = Hotel.objects.all()

#     def check_in_count(self, hotel: Hotel, date):
#         """
#         number of check_in in the specified date
#         """
#         return Reserve.objects.filter(room__hotel=hotel, start_day=date).count()

#     def check_out_count(self, hotel: Hotel, date):
#         """
#         number of check_out in the specified date
#         """
#         return Reserve.objects.filter(room__hotel=hotel, end_day=date).count()

#     def people_count(self, hotel: Hotel, date):
#         """
#         number of people(based on reserved rooms) in the specified date
#         """
#         reserves = Reserve.objects.filter(room__hotel=hotel, start_day__lte=date,
#                                           end_day__gt=date).select_related('room').all()
#         # print('people count: ', reserves)
#         count = 0

#         for r in reserves:
#             count += r.room.sleeps

#         return count

#     def full_empty_rooms_spaces(self, hotel: Hotel, date):
#         """
#         number of reserved and no completely reserved room(check_in date until the day before check_out)
#         in the specified date
#         """
#         rooms = hotel.rooms.prefetch_related('spaces').all()
#         reserved_spaces = (Reserve.objects.filter(room__in=rooms, start_day__lte=date, end_day__gt=date)
#                            .values_list('roomspace').all())
#         reserved_spaces = [r for tup in reserved_spaces for r in tup]

#         # print("full_rooms  ,rs: ", reserved_spaces)
#         full_spaces = {r.type: [] for r in rooms}
#         empty_spaces = {r.type: [] for r in rooms}
#         full_rooms = []
#         not_full_rooms = []
#         for r in rooms:
#             full = True
#             for s in r.spaces.all():
#                 # print('space_id: ', s.id)
#                 if not (s.id in reserved_spaces):
#                     full = False
#                     empty_spaces[r.type].append(s)
#                 else:
#                     full_spaces[r.type].append(s)

#             if full:
#                 full_rooms.append(r)
#             else:
#                 not_full_rooms.append(r)

#         fr = PublicRoomSerializer(full_rooms, many=True)
#         nfr = PublicRoomSerializer(not_full_rooms, many=True)

#         fs = {r.type: RoomSpaceSerializer(full_spaces[r.type], many=True).data for r in rooms}
#         es = {r.type: RoomSpaceSerializer(empty_spaces[r.type], many=True).data for r in rooms}

#         # s_count = (len(empty_spaces[r.type]) + len(full_spaces[r.type]))
#         # if s_count < 1:
#         #     s_count = 1
#         percent = {
#             ro.type: (len(full_spaces[ro.type]) / max((len(empty_spaces[ro.type]) + len(full_spaces[ro.type])),
#                                                       1) * 100)
#             for ro in rooms}
#         return {"rooms": {"full": fr.data, "not_full": nfr.data}, 'spaces': {'full': fs, 'empty': es},
#                 'percent': percent}

#     def room_type_count(self, dic):
#         """
#         count number of all spaces and full spaces from 'full_empty_rooms_spaces()' output
#         dic: this the output of function 'full_empty_rooms_spaces()'
#         """
#         spaces = dic['spaces']
#         type_count = {}
#         for r_type in spaces['full'].keys():
#             # print("in room type count, spaces", spaces['full'])
#             full_nums = len(spaces['full'][r_type])
#             empty_nums = len(spaces['empty'][r_type])
#             type_count[r_type] = {"fullRooms": full_nums, "allRooms": empty_nums + full_nums}

#         return type_count

#     def room_count(self, hotel: Hotel):
#         rooms = hotel.rooms.all()
#         count = 0
#         for r in rooms:
#             count += r.spaces.count()
#         return count

#     def reserve_days_count(self, reserve: Reserve):
#         return (reserve.end_day - reserve.start_day).days

#     def reserve_month_past(self, reserve: Reserve, date):
#         diff = reserve.start_day
#         if date - relativedelta(month=6) <= diff < date - relativedelta(month=5):
#             return 0
#         elif date - relativedelta(month=5) <= diff < date - relativedelta(month=4):
#             return 1
#         elif date - relativedelta(month=4) <= diff < date - relativedelta(month=3):
#             return 2
#         elif date - relativedelta(month=3) <= diff < date - relativedelta(month=2):
#             return 3
#         elif date - relativedelta(month=2) <= diff < date - relativedelta(month=1):
#             return 4
#         elif date - relativedelta(month=1) <= diff < date - relativedelta(month=0):
#             return 5
#         else:
#             return -1

#     def reserves_income_status(self, hotel: Hotel, date):
#         """
#         return past 6 month income and #reserves
#         """

#         income = [0] * 6
#         reserve = [0] * 6

#         rooms = hotel.rooms.all()
#         reserves = Reserve.objects.filter(start_day__gte=date - relativedelta(months=6)
#                                           , start_day__lt=date, room__in=rooms).all()
#         # print("reserve income, reserves past 6m: ", reserves, "\n date: ", date - relativedelta(months=0))
#         for r in reserves:
#             i = self.reserve_month_past(r, date)
#             day_count = self.reserve_days_count(r)
#             p = day_count * r.price_per_day
#             reserve[i] += 1
#             income[i] += p

#         return {'incomes': income, 'reserves': reserve}

#     def retrieve(self, request, *args, **kwargs):
#         # self.get_permissions()

#         self.check_permissions(request)
#         # print()

#         try:
#             hotel: Hotel = get_object_or_404(Hotel.objects.prefetch_related('rooms').filter(pk=kwargs.get('pk')))
#         except:
#             return Response("URL Not Valid", status=http.HTTPStatus.BAD_REQUEST)

#         try:
#             self.check_permissions(request)
#             self.check_object_permissions(request, hotel)
#         except:
#             return Response("Do Not Have Permission", status=http.HTTPStatus.FORBIDDEN)

#         # hotel: Hotel = get_object_or_404(Hotel, pk=int(kwargs.get('pk')))
#         try:
#             date = parse_date(request.query_params.get('date', None))
#             if date is None:
#                 date = datetime.today().date()

#         except:
#             # return Response("Date Not Valid", status=http.HTTPStatus.BAD_REQUEST)
#             date = datetime.today().date()

#         stat = self.full_empty_rooms_spaces(hotel, date)

#         rooms_count = self.room_type_count(stat)

#         res_stat = self.reserves_income_status(hotel, date)

#         data = {
#             'date': date,
#             'people_in_hotel': self.people_count(hotel, date),
#             'spaces_status': stat['spaces'],
#             'spaces_percentage': stat['percent'],
#             "rooms_status": stat['rooms'],
#             "room_types_count": rooms_count,
#             'room_count': self.room_count(hotel),
#             'check_in_count': self.check_in_count(hotel, date),
#             'check_out_count': self.check_out_count(hotel, date),
#             'reserves': res_stat['reserves'],
#             'incomes': res_stat['incomes'],

#         }

#         return Response(data, status=http.HTTPStatus.OK)


# class NewHotelViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = BestHotelSerializer

#     def get_queryset(self):
#         queryset = Hotel.objects.order_by('-rate')[0:10]
#         return queryset
