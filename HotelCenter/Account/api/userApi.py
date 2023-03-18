# from ..models import User
# from ..serializers.user_serializers import PublicUserSerializer, MyProfileSerializer
# from rest_framework.response import Response
# from rest_framework import generics
# from rest_framework import viewsets
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status


# class publicUserList(viewsets.ViewSet, generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = PublicUserSerializer

# class publicUserDetail(viewsets.ViewSet, generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = PublicUserSerializer

# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
# def myProfileDetail(request):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     user = request.user

#     if request.method == 'GET':
#         serializer = MyProfileSerializer(user)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = MyProfileSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)