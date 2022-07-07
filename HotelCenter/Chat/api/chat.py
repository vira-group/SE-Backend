from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from Hotel.models import Hotel
from ..models import Message, HotelChat
from ..serializers.chat_serializer import MessageSerializer, HotelChatSerializer
import numpy as np
from django.shortcuts import get_object_or_404

class MessageAPI(APIView):
    def post(self, request):
        pass


# class UserChatList(APIView):

#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         messages = Message.objects.all()
#         chatlist = []
#         for message in messages:
#             if(self.isvalid(message.chat, str(request.user.id))):
#                 if(not message in chatlist):
#                     chatlist.append(message)
#         serializer = MessageSerializer(chatlist, many=True)
#         return Response(serializer.data)

#     def isvalid(self, chatname, id):
#         try:
#             if (chatname.split("t")[1]==id or chatname.split("t")[0] == id ):
#                 return True
#             return False
#         except:
#             return False

class UserChatList(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        chatlist = HotelChat.objects.filter(user = user).all()
        serializer = HotelChatSerializer(chatlist, many=True) 
        return Response(serializer.data)




class HotelChatAPI(APIView):
    def get(self, request, hotel_id, format=None):
        try:
            hotel = get_object_or_404(Hotel, id = hotel_id )
            hotel_chat = get_object_or_404(HotelChat, hotel=hotel , user=request.user)
            serializer = HotelChatSerializer(hotel_chat) 
            return Response(serializer.data)
        except:
            hotel = get_object_or_404(Hotel, id = hotel_id )
            hotel_chat = HotelChat.objects.create(roomname = np.random.randint(0,99999), hotel = hotel, user=request.user)
            serializer = HotelChatSerializer(hotel_chat) 
            return Response(serializer.data)


class HotelChatList(APIView):
    def get(self, request, hotel_id, format=None):
        hotel = get_object_or_404(Hotel, id = hotel_id )
        if(request.user == hotel.creator or request.user in hotel.editors.all()):
            chatlist = HotelChat.objects.filter(hotel = hotel).all()
            serializer = HotelChatSerializer(chatlist, many=True) 
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)

