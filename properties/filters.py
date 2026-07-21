import django_filters

from .models import Property


class PropertyFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name='price_per_night',
        lookup_expr='gte'
    )

    max_price = django_filters.NumberFilter(
        field_name='price_per_night',
        lookup_expr='lte'
    )


    class Meta:
        model = Property

        fields = [
            'property_type',
            'location',
            'room_count',
            'min_price',
            'max_price'
        ]