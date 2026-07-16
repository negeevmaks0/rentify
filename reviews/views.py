from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Review
from .serializers import ReviewSerializer

from users.permissions import IsReviewAuthorOrReadOnly
from properties.permissions import IsTenant


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )


    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsTenant]

        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsReviewAuthorOrReadOnly]

        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
