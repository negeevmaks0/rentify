from rest_framework import serializers

from .models import Booking
from properties.models import Property
from properties.serializers import PropertySerializer

from datetime import timedelta
from django.utils import timezone


class BookingSerializer(serializers.ModelSerializer):
    booking_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    tenant = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    tenant_username = serializers.CharField(
        source="tenant.username",
        read_only=True
    )

    cancellation_deadline = serializers.DateField(
        read_only=True
    )

    status = serializers.CharField(
        read_only=True
    )

    property_detail = PropertySerializer(
        source="property",
        read_only=True
    )

    nights = serializers.SerializerMethodField()
    can_manage = serializers.SerializerMethodField()


    def get_can_manage(self, obj):
        request = self.context["request"]

        return obj.property.owner == request.user


    def get_nights(self, obj):
        return (obj.end_date - obj.start_date).days


    def create(self, validated_data):
        request = self.context['request']

        property = validated_data['property']

        start_date = validated_data['start_date']
        nights = (validated_data['end_date'] - start_date).days

        if nights <= 0:
            raise serializers.ValidationError(
                "Booking must contain at least one night."
            )

        deadline = start_date - timedelta(days=2)

        if deadline < timezone.now().date():
            deadline = timezone.now().date()

        
        validated_data['tenant'] = request.user
        validated_data['booking_price'] = property.price_per_night * nights
        validated_data['cancellation_deadline'] = deadline

        return Booking.objects.create(**validated_data)


    def validate(self, data):
        request = self.context['request']

        if request.user.role != "tenant":
            raise serializers.ValidationError(
                "Only tenants can create bookings."
            )

        start_date = data['start_date']
        end_date = data['end_date']
        property = data['property']


        if property.owner == request.user:
            raise serializers.ValidationError('You cannot book your own property.')

        if not property.is_active:
            raise serializers.ValidationError('This property is not available.')

        today = timezone.now().date()

        if start_date < today:
            raise serializers.ValidationError("Booking cannot start in the past.")

        if end_date <= start_date:
            raise serializers.ValidationError(
                "Booking must contain at least one night."
            )

        exists = Booking.objects.filter(
            property=property,
            status='approved',
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exists()

        if exists:
            raise serializers.ValidationError("This property is already booked for these dates.")

        return data


    class Meta:
        model = Booking

        fields = (
            'id',
            'property',
            'property_detail',
            'tenant',
            'tenant_username',
            'start_date',
            'end_date',
            'can_manage',
            'nights',
            'booking_date',
            'cancellation_deadline',
            'status',
            'booking_price'
        )

        read_only_fields = (
            'tenant',
            'booking_date',
            'cancellation_deadline',
            'booking_price',
            'status'
        )
