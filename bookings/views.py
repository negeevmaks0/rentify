from rest_framework import viewsets, status

from rest_framework.decorators import action
from rest_framework.response import Response

from properties.permissions import IsLandlord, IsTenant
from .permissions import IsBookingOwner, IsPropertyOwner

from .models import Booking
from .serializers import BookingSerializer

from django.utils import timezone
from django.shortcuts import render

# Create your views here.

def booking_create_page(request, property_id):
    return render(
        request,
        "bookings/create.html",
        {"property_id": property_id}
    )


def booking_list_page(request):
    return render(
        request,
        "bookings/list.html"
    )


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer

    def get_queryset(self):
        user = self.request.user
        booking_filter = self.request.query_params.get("filter")
        today = timezone.now().date()

        if user.role == 'tenant':
            queryset = Booking.objects.filter(tenant=user)

            if booking_filter == "active":
                queryset = queryset.filter(
                    end_date__gte=today,
                    status__in=["pending", "approved"]
                )

            elif booking_filter == "completed":
                queryset = queryset.filter(status="completed")

            elif booking_filter == "cancelled":
                queryset = queryset.filter(status="cancelled")

            elif booking_filter == "rejected":
                queryset = queryset.filter(status="rejected")

            elif booking_filter == "pending":
                queryset = queryset.filter(status="pending")

            elif booking_filter == "approved":
                queryset = queryset.filter(status="approved")

            elif booking_filter in [None, ""]:
                queryset = queryset.filter(
                    status__in=[
                        "pending",
                        "approved",
                        "completed",
                        "rejected",
                        "cancelled"
                    ]
                )

            return queryset

        if user.role == 'landlord':
            queryset = Booking.objects.filter(property__owner=user)

            if booking_filter == "pending":
                queryset = queryset.filter(status="pending")

            elif booking_filter == "approved":
                queryset = queryset.filter(status="approved")

            elif booking_filter == "rejected":
                queryset = queryset.filter(status="rejected")

            return queryset

        return Booking.objects.none()


    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsTenant]

        elif self.action in ['approve', 'reject']:
            permission_classes = [IsLandlord, IsPropertyOwner]

        elif self.action == 'cancel':
            permission_classes = [IsTenant, IsBookingOwner]

        else:
            permission_classes = [IsTenant | IsLandlord]

        return [permission() for permission in permission_classes]


    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        booking = self.get_object()

        if booking.property.owner != request.user:
            return Response(
                {"detail":"You cannot manage this booking."},
                status=403
            )

        if booking.status != "approved":
            return Response(
                {"detail":"Only approved bookings can be completed."},
                status=400
            )

        booking.status = "completed"
        booking.save()

        return Response({"status":"completed"})


    @action(detail=True, methods=['patch'])
    def approve(self, request, pk=None):
        booking = self.get_object()

        if booking.property.owner != request.user:
            return Response(
                {"detail": "You are not the owner of this property"},
                status=status.HTTP_403_FORBIDDEN
            )

        if booking.status != 'pending':
            return Response(
                {"detail": "Only pending bookings can be approved."},
                status=status.HTTP_400_BAD_REQUEST
            )

        overlap = Booking.objects.filter(
            property=booking.property,
            status="approved",
            start_date__lt=booking.end_date,
            end_date__gt=booking.start_date
        ).exclude(id=booking.id).exists()

        if overlap:
            return Response(
                {"detail": "Another approved booking exists for these dates."},
                status=status.HTTP_400_BAD_REQUEST
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
                status=403
            )

        if booking.status != 'pending':
            return Response(
                {"detail": "Only pending bookings can be rejected."},
                status=status.HTTP_400_BAD_REQUEST
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


    @action(detail=False, methods=['get'])
    def history(self, request):
        bookings = self.get_queryset().filter(end_date__lt=timezone.now().date())
        serializer = self.get_serializer(bookings, many=True)

        return Response(serializer.data)
