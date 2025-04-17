import django_filters
from .models import Property


class PropertyFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_rooms = django_filters.NumberFilter(field_name='rooms', lookup_expr='gte')
    max_rooms = django_filters.NumberFilter(field_name='rooms', lookup_expr='lte')
    city = django_filters.CharFilter(field_name='location__city', lookup_expr='icontains')
    district = django_filters.CharFilter(field_name='location__district', lookup_expr='icontains')
    property_type = django_filters.NumberFilter(field_name='property_type')

    class Meta:
        model = Property
        fields = [
            'min_price', 'max_price', 'min_rooms', 'max_rooms',
            'city', 'district', 'property_type', 'status'
        ]