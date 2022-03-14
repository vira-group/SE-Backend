from rest_framework import viewsets, permissions

from ..permissions import *
from ..models import Hotel, Facility
from ..serializers.hotel_serializers import HotelSerializer, FacilitiesSerializer


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }


class FacilityViewSet(viewsets.mixins.ListModelMixin):
    queryset = Facility.objects.all()
    serializer_class = FacilitiesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
