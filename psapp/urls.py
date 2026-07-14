from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    PropertyViewSet,
    PropertyImageViewSet,
    BookingViewSet,
    ReviewViewSet
)



router = DefaultRouter()

router.register('users', UserViewSet)
router.register('properties', PropertyViewSet)
router.register('images', PropertyImageViewSet)
router.register('bookings', BookingViewSet)
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

