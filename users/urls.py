from django.urls import path

from .views import RegisterView, ProfileView, LoginView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)



urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),

    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
