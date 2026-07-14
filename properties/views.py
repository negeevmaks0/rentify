from .serializers import PropertySerializer, PropertyImageSerializer
from .models import Property, PropertyImage

from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated
from .permissions import IsLandlord

from rest_framework import viewsets

# Create your views here.


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    )

    search_fields = (
        'title',
        'description',
        'location'
    )

    filterset_fields = (
        'property_type',
        'location',
        'room_count',
        'price_per_month'
    )

    ordering_fields = (
        'price_per_month',
        'created_at'
    )

    def get_permissions(self):
        if self.action in [
            'create',
            'update',
            'partial_update',
            'destroy'
        ]:
            permission_classes = [
                IsLandlord
            ]

        else:
            permission_classes = [
                IsAuthenticated
            ]

        return [
            permission()
            for permission in permission_classes
        ]


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class PropertyImageViewSet(viewsets.ModelViewSet):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer
