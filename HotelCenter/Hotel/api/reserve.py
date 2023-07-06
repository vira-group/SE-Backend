import http
from http.client import FORBIDDEN
from django.http import HttpResponseForbidden

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.utils.timezone import datetime
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from ..filter_backends import *
from ..permissions import *
from ..models import CancelReserve, Reserve, Room
from ..serializers.reserve_serializers import CancelReserveSerializer, RoomReserveSerializer, AdminReserverSerializer
from ..tasks import set_reserve_tasks
# from HotelCenter.permissions import IsManager, IsCustomer


class ReserveList(APIView):
    permission_classes = [IsAuthenticated ]

    def get(self, request):
        reserveList = Reserve.objects.filter(user=request.user)
        serializer = RoomReserveSerializer(reserveList, many=True)
        return Response(serializer.data)

    def post(self, request, room_id):

        user = request.user
        room = get_object_or_404(Room, id=room_id)
        serializer = RoomReserveSerializer(data=request.data)
        hotel = room.hotel
        manager = hotel.manager

        if serializer.is_valid():
            today = datetime.today()
            if (today.date() > serializer.validated_data["check_in"] or serializer.validated_data["check_in"] >
                    serializer.validated_data["check_out"]):
                return Response('dates not valid', status=status.HTTP_403_FORBIDDEN)
            if (request.user.balance < (
                    (serializer.validated_data["check_out"] - serializer.validated_data["check_in"]).days + 1) *
                    room.price):
                return Response(data='credit Not enough', status=status.HTTP_406_NOT_ACCEPTABLE)

            if (checkCondition(room, serializer.validated_data["check_in"],
                                serializer.validated_data["check_out"])):

                total_price = calculate_totalprice(serializer.validated_data,room)                
                res = serializer.save(user=user, room=room, total_price=total_price)
                
                user.balance -= total_price
                user.save()

                manager.balance += total_price
                manager.save()

                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response("not enough space", status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def calculate_totalprice(validated_data,room):
    check_in = validated_data["check_in"]
    check_out = validated_data["check_out"]
    total_days = ((check_out - check_in).days +1)
    total_price = total_days * room.price
    return total_price

def checkCondition(room, start, end):
    room_reserve_list = Reserve.objects.filter(room=room).all()
    for room_reserve in room_reserve_list:
        if ((room_reserve.check_in <= start <= room_reserve.check_out) or (
                room_reserve.check_in <= end <= room_reserve.check_out)):
            return False
    return True

class MyReservesViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    serializer_class = RoomReserveSerializer
    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super(MyReservesViewSet, self).dispatch(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        user = request.user
        reserves = list(Reserve.objects.filter(user_id=user.id).all())
        reserve_data = self.serializer_class(instance=reserves, many=True)
        data = { 'reserves' : reserve_data.data }
        return Response(data=data, status=http.HTTPStatus.OK)

class AdminReserveViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated, IsUrlHotelEditor)
    filterset_class = AdminReserveFilter
    serializer_class = AdminReserverSerializer

    def get_queryset(self):
        query_set = Reserve.objects.filter(room__hotel_id=self.kwargs['hid']).all()

        return query_set


class UserCancelReserveList(APIView):
    permission_classes = [IsAuthenticated ]

    def post(self, request):
        user = request.user
        reserve_id = request.data['reserve']
        reserve = get_object_or_404(Reserve, id=reserve_id)
        serializer = CancelReserveSerializer(data=request.data)
        if serializer.is_valid():
            if user == reserve.user:
                today = datetime.today()
                if (today.date() > reserve.check_in):
                    return Response('invalid', status=status.HTTP_403_FORBIDDEN)
                
                # roomspace -> room
                serializer.save(reserve=reserve_id, check_in=reserve.check_in, check_out=reserve.check_out,
                                user=user, room=reserve.room, price_per_day=reserve.price_per_day,
                                firstname=reserve.firstname,
                                lastname=reserve.lastname, national_code=reserve.national_code,
                                phone_number=reserve.phone_number)
                
                user.balance += ((reserve.check_out - reserve.check_in).days + 1) * reserve.price_per_day
                user.save()
                reserve.delete()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)