from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..models import Message
from ..serializers.chat_serializer import MessageSerializer

class MessageAPI(APIView):
    def post(self, request):
        pass


class UserChatList(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        messages = Message.objects.all()
        chatlist = []
        for message in messages:
            if(self.isvalid(message.chat, str(request.user.id))):
                if(not message in chatlist):
                    chatlist.append(message)
        serializer = MessageSerializer(chatlist, many=True)
        return Response(serializer.data)

    def isvalid(self, chatname, id):
        try:
            if (chatname.split("t")[1]==id or chatname.split("t")[0] == id ):
                return True
            return False
        except:
            return False
