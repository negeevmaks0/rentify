from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PropertyViewSet, PropertyImageViewSet

router = DefaultRouter()
router.register('', PropertyViewSet, basename='property')
router.register('images', PropertyImageViewSet, basename='property-image')

urlpatterns = [
    path('', include(router.urls)),
]