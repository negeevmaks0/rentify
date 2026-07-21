from .models import Property, PropertyImage
from users.serializers import UserSerializer
from reviews.serializers import PropertyReviewSerializer
from reviews.models import Review

from rest_framework import serializers


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage

        fields = (
            'id',
            'property',
            'image'
        )


    def validate_property(self, value):
        request = self.context['request']

        if value.owner != request.user:
            raise serializers.ValidationError('Youcan upload images only to your own properties.')

        return value


class PropertySerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    images = PropertyImageSerializer(many=True, read_only=True)
    main_image = serializers.SerializerMethodField()

    reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    def get_reviews_count(self, obj):
        return Review.objects.filter(
            booking__property=obj
        ).count()


    def get_reviews(self, obj):
        reviews = Review.objects.filter(
            booking__property=obj
        ).order_by(
            '-created_at'
        )[:6]

        return PropertyReviewSerializer(
            reviews,
            many=True
        ).data



    def get_average_rating(self, obj):
        reviews = Review.objects.filter(
            booking__property=obj
        )

        if not reviews.exists():
            return 0

        return round(
            sum(
                review.rating
                for review in reviews
            ) / reviews.count(),
            1
        )

    class Meta:
        model = Property

        fields = (
            'id',
            'owner',
            'title',
            'description',
            'location',
            'price_per_night',
            'room_count',
            'property_type',
            'is_active',
            'created_at',
            'images',
            'main_image',
            'reviews',
            'average_rating',
            'reviews_count',
        )

    def get_main_image(self, obj):
        image = obj.images.first()

        if image:
            return image.image.url

        return None

    read_only_fields = (
        'owner',
        'created_at'
    )