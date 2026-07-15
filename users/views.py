from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView

from .models import User
from .serializers import UserSerializer, RegisterSerializer

# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()



class ProfileView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
