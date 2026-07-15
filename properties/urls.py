from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import PropertyViewSet, PropertyImageViewSet



router = DefaultRouter()

router.register('', PropertyViewSet, basename='property')
router.register('images', PropertyImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
