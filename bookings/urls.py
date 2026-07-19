from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import booking_create_page



router = DefaultRouter()

urlpatterns = [
    path(
        "create/<int:property_id>/",
        booking_create_page,
        name="booking_create"
    ),
]
