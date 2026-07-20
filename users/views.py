from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from django.views.generic import TemplateView

# Create your views here.

def set_token_cookies(response, user):
    refresh = RefreshToken.for_user(user)

    response.set_cookie(
        'access_token',
        str(refresh.access_token),
        httponly=True,
        samesite='Lax'
    )

    response.set_cookie(
        'refresh_token',
        str(refresh),
        httponly=True,
        samesite='Lax'
    )

    return response


class LoginPageView(TemplateView):
    template_name = 'users/login.html'


class RegisterPageView(TemplateView):
    template_name = 'users/register.html'


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        response = Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

        return set_token_cookies(response, user)


class ProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response(
            {"detail": "Logged out"},
            status=status.HTTP_200_OK
        )

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        response = Response(
            UserSerializer(user).data,
            status=status.HTTP_200_OK
        )

        return set_token_cookies(response, user)
