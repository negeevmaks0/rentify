from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    booking_create_page,
    booking_list_page
)



router = DefaultRouter()

urlpatterns = [
    path(
        "create/<int:property_id>/",
        booking_create_page,
        name="booking_create"
    ),

    path(
        "",
        booking_list_page,
        name="booking_list"
    ),
]