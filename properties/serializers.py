from .models import Property, PropertyImage
from users.serializers import UserSerializer

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
            'main_image'
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