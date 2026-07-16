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


    class Meta:
        model = Property

        fields = '__all__'

        read_only_fields = (
            'owner',
            'created_at'
        )