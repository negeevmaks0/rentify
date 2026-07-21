from rest_framework import serializers

from .models import Review
from bookings.models import Booking


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all())

    class Meta:
        model = Review

        fields = (
            'id',
            'booking',
            'author',
            'rating',
            'comment',
            'created_at'
        )

        read_only_fields = (
            'author',
            'created_at'
        )


    def validate_booking(self, booking):
        user = self.context['request'].user

        if booking.tenant != user:
            raise serializers.ValidationError('You can review only your own booking.')

        if booking.status != 'completed':
            raise serializers.ValidationError(
                'You can review only completed bookings.'
            )

        if hasattr(booking, 'review'):
            raise serializers.ValidationError('This booking already has a review.')

        return booking


    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user

        return Review.objects.create(**validated_data)
