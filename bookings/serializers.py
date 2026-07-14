from rest_framework import serializers
from .models import Booking

from datetime import timedelta
from django.utils import timezone



class BookingSerializer(serializers.ModelSerializer):
    booking_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    tenant = serializers.PrimaryKeyRelatedField(read_only=True)
    cancellation_deadline = serializers.DateField(read_only=True)

    def create(self, validated_data):
        request = self.context['request']

        property = validated_data['property']
        start_date = validated_data['start_date']

        validated_data['tenant'] = request.user
        validated_data['booking_price'] = property.price_per_month
        validated_data['cancellation_deadline'] = (start_date - timedelta(days=2))

        return Booking.objects.create(**validated_data)



    def validate(self, data):
        start_date = data['start_date']
        end_date = data['end_date']
        property = data['property']

        today = timezone.now().date()

        if start_date < today:
            raise serializers.ValidationError("Booking cannot start in the past.")

        if start_date > end_date:
            raise serializers.ValidationError("End date must be after start date.")

        exists = Booking.objects.filter(
            property=property,
            status='approved',
            start_date__lte=end_date,
            end_date__gte=start_date
        ).exists()

        if exists:
            raise serializers.ValidationError("This property is already booked for these dates.")

        return data



    class Meta:
        model = Booking

        fields = (
            'id',
            'property',
            'tenant',
            'start_date',
            'end_date',
            'booking_date',
            'cancellation_deadline',
            'status',
            'booking_price'
        )
