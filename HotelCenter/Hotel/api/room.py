from email import message
from django.shortcuts import get_object_or_404
from Hotel.models import Room
from Hotel.serializers.room_serializers import PublicRoomSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from Hotel.models import Hotel

class RoomList( APIView):

    def get(self, request, hotel_id, format=None):
        hotel = get_object_or_404(Hotel, id=hotel_id)
        rooms = Room.objects.filter(hotel = hotel)
        serializer = PublicRoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request, hotel_id, format=None):
        hotel = get_object_or_404(Hotel, id=hotel_id)
        serializer = PublicRoomSerializer(data=request.data)
        if (not request.user == hotel.creator) and (not request.user in hotel.editors) :
            return Response(serializer.data ,status=status.HTTP_403_FORBIDDEN, message="You can not add a room to this hotel")
        else:
            if serializer.is_valid():
                serializer.save(hotel = hotel)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)