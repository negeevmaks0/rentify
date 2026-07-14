from rest_framework import serializers
from .models import User, Property, PropertyImage, Booking, Review



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'role'
        )



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)


    class Meta:
        model = User

        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'role'
        )


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage

        fields = '__all__'



class PropertySerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='owner',
        write_only=True
    )

    images = PropertyImageSerializer(many=True, read_only=True)


    class Meta:
        model = Property

        fields = (
            'id',
            'owner',
            'owner_id',
            'title',
            'description',
            'location',
            'price_per_month',
            'room_count',
            'property_type',
            'is_active',
            'created_at',
            'images'
        )



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking

        fields = '__all__'



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review

        fields = '__all__'
