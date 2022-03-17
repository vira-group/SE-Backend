from rest_framework import viewsets, permissions, \
    filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from ..permissions import *
from ..models import Hotel, Facility
from ..serializers.hotel_serializers import HotelSerializer, FacilitiesSerializer


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['city', 'state']
    filterset_fields = ['name']

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def create(self, request, *args, **kwargs):
        """
            if current user does not have a hotel already create a hotel
        """
        if Hotel.objects.filter(creator=request.user).count() > 0:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': "Already Have A Hotel."}
                            , content_type='json')
        else:
            request.data
            return super().create(request, *args, **kwargs)


class FacilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitiesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
