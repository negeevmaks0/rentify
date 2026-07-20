from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


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


class LoginSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        attrs['username'] = attrs.get('email')

        return super().validate(attrs)
