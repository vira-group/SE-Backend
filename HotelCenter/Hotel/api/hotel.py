import http

# import rest_framework.request
from rest_framework import viewsets, permissions, \
    filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from ..permissions import *
from ..models import Hotel, Facility, HotelImage
from ..serializers.hotel_serializers import HotelSerializer, FacilitiesSerializer, HotelImgSerializer


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


class HotelImgViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin,
                      viewsets.mixins.CreateModelMixin, viewsets.mixins.DestroyModelMixin):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsEditorOrReadOnly]
    serializer_class = HotelImgSerializer

    def get_queryset(self):
        self.queryset = HotelImage.objects.filter(hotel_id=self.h_id).all()
        return self.queryset

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def dispatch(self, request, *args, **kwargs):
        self.request = request

        try:
            self.h_id = int(kwargs.get('hid'))
            self.req_hotel: Hotel = Hotel.objects.get(pk=self.h_id)
        except:
            return Response("hotel not found", status=http.HTTPStatus.NOT_FOUND)

        return super().dispatch(request, *args, **kwargs)

    def create(self, request: rest_framework.request.Request, *args, **kwargs):
        """
        if is_header==true:
            set hotel.header to request.files[image]
        else
            add new image to hotel images
        """

        print(self.req_hotel.header.url)

        is_header = request.GET.get("is_header", None)
        if is_header == 'true':

            try:
                # self.req_hotel.header = request.FILES['image']
                img = request.FILES['image']
                self.req_hotel = Hotel.objects.get(pk=self.h_id)
                self.req_hotel.header = img
                self.req_hotel.save()
                print('change header')
                # self.req_hotel.header = request.FILES['image']

                return Response(HotelSerializer(self.req_hotel).data, 200)
            except:
                print(' in is header')
                return Response("file not valid", http.HTTPStatus.BAD_REQUEST)

        hotelimg = HotelImgSerializer(request.FILES)
        try:
            print("image\n", request.FILES['image'])
            print(hotelimg.is_valid(raise_exception=True))
            print('not saved\n', hotelimg['image'])
            img = hotelimg.save()
            print("img saved\n", img)
            return Response(img, status=http.HTTPStatus.OK)
        except:
            print('in image', hotelimg)
            return Response("file not valid", http.HTTPStatus.BAD_REQUEST)


class BestHotelViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # queryset = Hotel.objects.order(rate).all()
    serializer_class = HotelSerializer

    def dispatch(self, request: rest_framework.request.Request, *args, **kwargs):
        self.request = request
        self.in_kwargs = kwargs
        self.count = int(request.GET.get('count'))

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = Hotel.objects.order_by('rate').all()[0:self.count]
        return self.queryset
