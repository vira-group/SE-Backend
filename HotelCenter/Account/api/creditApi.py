import http

from ..models import User
from ..serializers import PublicUserSerializer, MyProfileSerializer, CreditSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import status

class CreditViewSet(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin, viewsets.mixins.ListModelMixin):
    serializer_class = CreditSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):

        return Response({"balance": request.user.balance}, http.HTTPStatus.OK)

    def create(self, request, *args, **kwargs):
        """
        add credit to user account
        """
        data = self.serializer_class(data=request.data)
        try:
            data.is_valid(raise_exception=True)

            # print(data.data)
            credit = data.data['credit']
            request.user.balance += credit
            request.user.save()
            return Response(data={"message": f'credit {credit:.2f} R added to your account',
                                  "new_credit": request.user.balance}, status=status.HTTP_200_OK)

        except:
            return Response('Not valid transition', status=status.HTTP_400_BAD_REQUEST)
