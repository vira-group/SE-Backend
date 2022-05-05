from django.shortcuts import get_object_or_404
from ..models import Reserve, Room, RoomSpace
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.reserve_serializers import RoomReserveSerializer, ReserveSerializer
from rest_framework import status
from django.utils.timezone import datetime

class RoomspaceReserveList(APIView):
    def get(self, request, roomspace_id, format=None):
        roomspace = get_object_or_404(RoomSpace, id=roomspace_id)
        hotel = roomspace.room.hotel
        reserveList = Reserve.objects.filter(roomspace = roomspace)
        if (not request.user == hotel.creator) and (not request.user in hotel.editors.all()):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = RoomReserveSerializer(reserveList, many=True)
        return Response(serializer.data)




class ReserveList(APIView):
    def get(self, request):
        reserveList = Reserve.objects.filter(user =  request.user)
        serializer = ReserveSerializer(reserveList, many=True)
        return Response(serializer.data)
    def post(self, request):
        user = request.user
        room_id = request.data['room']
        room = get_object_or_404(Room, id=room_id)
        roomspace_list = RoomSpace.objects.filter(room = room).all()
        serializer = ReserveSerializer(data=request.data)
        if serializer.is_valid():
            today = datetime.today()
            if(today.date()>serializer.validated_data["start_day"] or serializer.validated_data["start_day"] > serializer.validated_data["end_day"]):
                return Response(status=status.HTTP_403_FORBIDDEN)
            for roomspace in roomspace_list:
                if(checkCondition(roomspace, serializer.validated_data["start_day"], serializer.validated_data["end_day"])):
                    serializer.save(user= user, roomspace=roomspace)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def checkCondition(roomspace, start, end):
    roomspace_reserve_list = Reserve.objects.filter(roomspace = roomspace).all()
    for roomspace_reserve in roomspace_reserve_list:
        if((roomspace_reserve.start_day <= start <= roomspace_reserve.end_day) or (roomspace_reserve.start_day <= end <= roomspace_reserve.end_day)):
            return False
    return True