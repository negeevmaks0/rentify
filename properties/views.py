from .serializers import PropertySerializer, PropertyImageSerializer
from .models import Property, PropertyImage

from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated
from .permissions import IsLandlord, IsOwnerOrReadOnly

from rest_framework import viewsets

# Create your views here.


class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer


    def get_queryset(self):
        user = self.request.user

        if user.role == 'landlord':
            return Property.objects.filter(owner=user)

        return Property.objects.filter(is_active=True)


    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsLandlord]

        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

        else:
            permission_classes = [IsAuthenticated]


        return [permission() for permission in permission_classes]


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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



class PropertyImageViewSet(viewsets.ModelViewSet):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer
