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
