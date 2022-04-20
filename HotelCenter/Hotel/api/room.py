from email import message
from django.shortcuts import get_object_or_404
from Hotel.models import Room, roomFacility, RoomImage
from Hotel.serializers.room_serializers import PublicRoomSerializer, roomFacilitiesSerializer, RoomImageSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
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
                room = serializer.save(hotel = hotel)
                for f in request.data.get('room_facilities', []):
                    if roomFacility.objects.filter(name=f['name']).count() > 0:
                        room.facilities.add(roomFacility.objects.get(pk=f['name']))
                        room.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class roomFacilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = roomFacility.objects.all()
    serializer_class = roomFacilitiesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ImageList( APIView):

    def get(self, request, room_id, format=None):
        room = get_object_or_404(Room, id=room_id)
        images = RoomImage.objects.filter(room = room)
        serializer = RoomImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, room_id, format=None):
        
        room = get_object_or_404(Room, id=room_id)
        serializer = RoomImageSerializer(data=request.data)
        if (not request.user == room.hotel.creator) and (not request.user in room.hotel.editors) :
            return Response(serializer.data ,status=status.HTTP_403_FORBIDDEN, message="You can not add a picture to this room")
        else:
            if serializer.is_valid():
                serializer.save(room = room)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)