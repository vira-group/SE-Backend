import http

from django.utils.datetime_safe import datetime
from rest_framework import viewsets, permissions, \
    filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from Hotel.models import Hotel

from ..models import Comment
from ..serializers.comment_serializers import Comment_serializer
from ..permissions import IsWriterOrReadOnly


class HotelCommentViewSet(viewsets.ModelViewSet):
    serializer_class = Comment_serializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsWriterOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.filter(hotel=self.kwargs["hid"]).all()[0:50]

        return queryset

    def add_reply(self, hotel: Hotel, comment: Comment):
        rep_count = hotel.reply_count
        av_rate = hotel.rate
        com_rate = comment.rate
        sum_rate = (av_rate * rep_count) + com_rate
        new_count = rep_count + 1
        new_rate = sum_rate / new_count
        hotel.rate = new_rate
        hotel.reply_count = new_count
        hotel.save()

    def delete_reply(self, hotel: Hotel, comment: Comment):
        rep_count = hotel.reply_count
        av_rate = hotel.rate
        com_rate = comment.rate

        sum_rate = (av_rate * rep_count) - com_rate
        new_count = max(rep_count - 1, 0)
        if new_count > 0:
            new_rate = sum_rate / new_count
        else:
            new_rate = 4
        hotel.rate = new_rate
        hotel.reply_count = new_count

    def update_reply(self, hotel: Hotel, comment: Comment, old_rate):
        rep_count = hotel.reply_count
        av_rate = hotel.rate
        com_rate = comment.rate

        sum_rate = (av_rate * rep_count) + com_rate - old_rate
        new_count = rep_count
        new_rate = sum_rate / new_count
        hotel.rate = new_rate

    def create(self, request, *args, **kwargs):
        """
        create new comment
        """
        try:
            hotel = Hotel.objects.get(pk=kwargs.get("hid"))
        except:
            return Response("Hotel Not Found", http.HTTPStatus.NOT_FOUND)

        request.data['hotel'] = hotel
        request.data['writer'] = request.user
        com = self.serializer_class(request.data)
        if com.is_valid():
            comm = com.save()
            self.add_reply(hotel, comm)
            return Response(comm.data, http.HTTPStatus.CREATED)

        else:
            return Response(com.errors, http.HTTPStatus.BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        delete comment
        """

        self.check_permissions(request)
        try:
            hotel = Hotel.objects.get(pk=kwargs.get("hid"))
        except:
            return Response("Hotel Not Found", http.HTTPStatus.NOT_FOUND)

        try:
            comment = Comment.objects.get(pk=kwargs.get("pk"), hotel=hotel)

        except:
            return Response("Comment Not Found", http.HTTPStatus.NOT_FOUND)

        self.check_object_permissions(request, comment)

        self.delete_reply(hotel, comment)
        comment.delete()
        return Response("Comment Deleted.", http.HTTPStatus.OK)

    def update(self, request, *args, **kwargs):
        """
        update comment
        """
        self.check_permissions(request)
        try:
            hotel = Hotel.objects.get(pk=kwargs.get("hid"))
        except:
            return Response("Hotel Not Found", http.HTTPStatus.NOT_FOUND)

        try:
            comment = Comment.objects.get(pk=kwargs.get("pk"), hotel=hotel)

        except:
            return Response("Comment Not Found", http.HTTPStatus.NOT_FOUND)

        self.check_object_permissions(request, comment)
        serializer = self.serializer_class(instance=comment, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
        else:
            return Response(serializer.errors, http.HTTPStatus.BAD_REQUEST)

        return Response(serializer.data, http.HTTPStatus.OK)


class UserHotelCommentViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    serializer_class = Comment_serializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsWriterOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.filter(writer=self.request.user, hotel=self.kwargs['hid']).all()
        return queryset
