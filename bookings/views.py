from rest_framework import viewsets, status

from rest_framework.decorators import action
from rest_framework.response import Response

from properties.permissions import IsLandlord, IsTenant

from .models import Booking
from .serializers import BookingSerializer

from django.utils import timezone

# Create your views here.

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer


    def get_queryset(self):

        user = self.request.user

        if user.role == 'tenant':
            return Booking.objects.filter(
                tenant=user
            )


        if user.role == 'landlord':
            return Booking.objects.filter(
                property__owner=user
            )


        return Booking.objects.none()


    def get_permissions(self):
        if self.action in ['approve', 'reject']:
            permission_classes = [IsLandlord]

        elif self.action in ['create', 'cancel']:
            permission_classes = [IsTenant]

        else:
            permission_classes = [IsTenant | IsLandlord]


        return [permission() for permission in permission_classes]


    @action(detail=True, methods=['patch'])
    def approve(self, request, pk=None):
        booking = self.get_object()

        if booking.property.owner != request.user:
            return Response(
                {"detail": "You are not the owner of this property"},
                status=status.HTTP_403_FORBIDDEN
            )


        booking.status = 'approved'
        booking.save()


        return Response({"status": "Booking approved"})


    @action(detail=True, methods=['patch'])
    def reject(self, request, pk=None):
        booking = self.get_object()

        if booking.property.owner != request.user:
            return Response(
                {"detail": "You are not the owner of this property"},
                status=status.HTTP_403_FORBIDDEN
            )

        booking.status = 'rejected'
        booking.save()

        return Response({"status": "Booking rejected"})


    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        booking = self.get_object()

        if booking.tenant != request.user:
            return Response(
                {"detail": "This is not your booking."},
                status=status.HTTP_403_FORBIDDEN
            )

        if booking.status != 'pending':
            return Response(
                {"detail": "Only pending bookings can be cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if timezone.now().date() > booking.cancellation_deadline:
            return Response(
                {"detail": "Cancellation deadline has passed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'cancelled'
        booking.save()

        return Response(
            {"status": "Booking cancelled."},
            status=status.HTTP_200_OK
        )
