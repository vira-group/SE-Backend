from django_filters import rest_framework as filters
from .models import Hotel


class HotelMinRateFilters(filters.FilterSet):
    min_rate = filters.NumberFilter(field_name="rate", lookup_expr='gte')
    name_contain = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Hotel
        fields = ['min_rate', 'name', 'rate', 'facilities', 'name_contain', 'rooms__facilities']
