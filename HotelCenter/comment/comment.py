from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from Hotel.models import Hotel
from .models import Comment
from .permissions import IsWriterOrReadOnly
from .serializers import CommentSerializer


class HotelCommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsWriterOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.filter(hotel=int(self.kwargs["hid"])).all()[0:50]
        # print("hotel comment queryset:", queryset)
        return queryset

    def add_reply(self, hotel: Hotel, comment: Comment):
        rep_count = hotel.reply_count
        av_rate = hotel.rate
        com_rate = float(comment.rate)
        sum_rate = float(av_rate * rep_count) + com_rate
        new_count = rep_count + 1
        new_rate = sum_rate / new_count
        hotel.rate = new_rate
        hotel.reply_count = new_count
        hotel.save()

    def delete_reply(self, hotel: Hotel, comment: Comment):
        rep_count = hotel.reply_count
        av_rate = hotel.rate
        com_rate = float(comment.rate)

        sum_rate = float(av_rate * rep_count) - com_rate
        new_count = max(rep_count - 1, 0)
        if new_count > 0:
            new_rate = sum_rate / new_count
        else:
            new_rate = 4
        hotel.rate = new_rate
        hotel.reply_count = new_count
        hotel.save()

    def update_reply(self, hotel: Hotel, comment: Comment, old_rate: float):
        rep_count = hotel.reply_count
        av_rate = hotel.rate
        com_rate = float(comment.rate)

        sum_rate = float(av_rate * rep_count) + com_rate - float(old_rate)
        new_count = rep_count
        new_rate = sum_rate / max(new_count, 1)
        hotel.rate = new_rate
        hotel.save()

    def create(self, request, *args, **kwargs):
        """
        create new comment
        """
        
        hotel =get_object_or_404(Hotel,pk=kwargs.get("hid"))
        data = request.data.copy()
        data['hotel'] = hotel.id
        data['writer'] = request.user.id
        com = self.serializer_class(data=data)
        com.is_valid(raise_exception=True)
        comm = com.save()
        self.add_reply(hotel, comm)
        return Response(com.data,status= status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """
        delete comment
        """

        self.check_permissions(request)
        hotel = get_object_or_404(Hotel,pk=kwargs.get('hid'))
        comment =get_object_or_404(Comment ,pk=kwargs.get("pk"), hotel=hotel)
        self.check_object_permissions(request, comment)
        self.delete_reply(hotel, comment)
        comment.delete()
        return Response("Comment Deleted.",status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        update comment
        """
        self.check_permissions(request)
        hotel =get_object_or_404(Hotel,pk=kwargs.get("hid"))
        comment = get_object_or_404(Comment ,pk=kwargs.get("pk"), hotel=hotel)
        old_rate = comment.rate
        self.check_object_permissions(request, comment)
        serializer = self.serializer_class(instance=comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        self.update_reply(hotel=hotel, comment=serializer.instance, old_rate=old_rate)
        return Response(serializer.data,status=status.HTTP_200_OK)


class UserHotelCommentViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsWriterOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.filter(writer=self.request.user, hotel=self.kwargs['hid']).all()
        return queryset
