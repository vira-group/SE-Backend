
from rest_framework import viewsets

from ..models import Hotel, Facility
from ..serializers.hotel_serializers import HotelSerializer


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = []
    # lookup_field = 'pk'
    #
    # def retrieve(self, request, *args, **kwargs):
    #     pass
    #
    # def dispatch(self, request, *args, **kwargs):
    #     pass
    #
    # def update(self, request, *args, **kwargs):
    #     pass
    #
    # def list(self, request, *args, **kwargs):
    #     pass

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }