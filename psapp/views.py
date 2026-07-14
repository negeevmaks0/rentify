from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from .permissions import IsLandlord

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import (
    User,
    Property,
    PropertyImage,
    Booking,
    Review
)

from .serializers import (
    UserSerializer,
    PropertySerializer,
    PropertyImageSerializer,
    BookingSerializer,
    ReviewSerializer,
    RegisterSerializer
)



class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



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



class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer



class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
