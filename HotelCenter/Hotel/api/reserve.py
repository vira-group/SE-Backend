from django.shortcuts import get_object_or_404
from ..models import Reserve, RoomSpace
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.reserve_serializers import ReserveSerializer
from rest_framework import status


class RoomspaceReserveList(APIView):
    def get(self, request, roomspace_id, format=None):
        roomspace = get_object_or_404(RoomSpace, id=roomspace_id)
        hotel = roomspace.room.hotel
        reserveList = Reserve.objects.filter(roomspace = roomspace)
        if (not request.user == hotel.creator) and (not request.user in hotel.editors.all()):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = ReserveSerializer(reserveList, many=True)
        return Response(serializer.data)
