from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend

from .models import Review
from .serializers import ReviewSerializer

from users.permissions import IsReviewAuthorOrReadOnly
from properties.permissions import IsTenant

from properties.models import Property


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['booking']


    def get_queryset(self):
        return Review.objects.select_related('booking', 'author')


    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsTenant]

        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsReviewAuthorOrReadOnly]

        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


    @action(detail=False, methods=['get'])
    def property_reviews(self, request):
        property_id = request.query_params.get('property')

        reviews = Review.objects.filter(booking__property_id=property_id)

        serializer = self.get_serializer(reviews, many=True)

        return Response(serializer.data)
