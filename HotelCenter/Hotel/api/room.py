from email import message
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework import viewsets
from rest_framework.exceptions import NotFound, PermissionDenied
import http

from ..filter_backends import AdminRoomSpaceFilter
from ..models import Room, roomFacility, RoomImage, RoomSpace
from ..permissions import IsRoomSpaceOwnerOrEditor, IsUrlHotelEditor
from ..serializers.room_serializers import (PublicRoomSerializer, roomFacilitiesSerializer, RoomImageSerializer,
                                            RoomSpaceSerializer)
from ..models import Hotel


class RoomList(APIView):

    def get(self, request, hotel_id, format=None):
        hotel = get_object_or_404(Hotel, id=hotel_id)
        rooms = Room.objects.filter(hotel=hotel)
        serializer = PublicRoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request, hotel_id, format=None):
        hotel = get_object_or_404(Hotel, id=hotel_id)
        serializer = PublicRoomSerializer(data=request.data)
        if (not request.user == hotel.creator) and (not request.user in hotel.editors.all()):
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            if serializer.is_valid():
                room = serializer.save(hotel=hotel)
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


class ImageList(APIView):

    def get(self, request, room_id, format=None):
        room = get_object_or_404(Room, id=room_id)
        images = RoomImage.objects.filter(room=room)
        serializer = RoomImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, room_id, format=None):

        room = get_object_or_404(Room, id=room_id)
        serializer = RoomImageSerializer(data=request.data)
        if (not request.user == room.hotel.creator) and (not request.user in room.hotel.editors):
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN,
                            message="You can not add a picture to this room")
        else:
            if serializer.is_valid():
                serializer.save(room=room)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomSpaceViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin,
                       viewsets.mixins.CreateModelMixin, viewsets.mixins.DestroyModelMixin,
                       viewsets.mixins.UpdateModelMixin):
    permission_classes = [permissions.IsAuthenticated, IsRoomSpaceOwnerOrEditor]
    serializer_class = RoomSpaceSerializer

    def get_queryset(self):
        queryset = RoomSpace.objects.filter(room_id=self.room_id).all()
        return queryset

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.room_id = kwargs['room_id']
        print('\nroom_id ', self.room_id)

        return super(RoomSpaceViewSet, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            room_id = int(kwargs['room_id'])
            room = Room.objects.get(pk=room_id)

        except:
            return Response('Room not found', status=http.HTTPStatus.NOT_FOUND)

        space = RoomSpaceSerializer(data=request.data)
        if space.is_valid():
            space.save(room=room)
            return Response(data=space.data, status=http.HTTPStatus.CREATED)
        else:
            return Response('content not valid', status=http.HTTPStatus.BAD_REQUEST)


class AdminRoomSpaceViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsUrlHotelEditor]
    filter_backends = [DjangoFilterBackend]
    serializer_class = RoomSpaceSerializer
    filterset_class = AdminRoomSpaceFilter

    def get_queryset(self):
        query_set = RoomSpace.objects.filter(room__hotel_id=self.kwargs['hid'])
        return query_set