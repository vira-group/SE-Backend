# from django_filters import rest_framework as filters
# from .models import Hotel, Reserve, RoomSpace, Room


# class HotelMinRateFilters(filters.FilterSet):
#     min_rate = filters.NumberFilter(field_name="rate", lookup_expr='gte')
#     name_contain = filters.CharFilter(field_name='name', lookup_expr='icontains')

#     class Meta:
#         model = Hotel
#         fields = ['min_rate', 'name', 'rate', 'facilities', 'name_contain', 'rooms__facilities']


# class AdminReserveFilter(filters.FilterSet):
#     start_before = filters.DateFilter(field_name='start_day', lookup_expr='lt')
#     start_after = filters.DateFilter(field_name='start_day', lookup_expr='gte')
#     end_before = filters.DateFilter(field_name='end_day', lookup_expr='lt')
#     end_after = filters.DateFilter(field_name='end_day', lookup_expr='gte')

#     class Meta:
#         model = Reserve
#         fields = ['room', 'roomspace', 'start_day', 'end_day', 'start_before', 'start_after', 'end_before', 'end_after']


# class AdminRoomSpaceFilter(filters.FilterSet):
#     name_start = filters.CharFilter(field_name='name', lookup_expr='startswith')
#     name_icontain = filters.CharFilter(field_name='name', lookup_expr='icontains')

#     class Meta:
#         model = RoomSpace
#         fields = ['room', 'name', 'name_start', 'name_icontain']


# class AdminRoomFilter(filters.FilterSet):
#     size = filters.RangeFilter(field_name='size')
#     class Meta:
#         model = Room
#         fields = ['type', 'sleeps', 'option', 'size', 'view']
