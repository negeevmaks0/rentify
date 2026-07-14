from django.contrib import admin

from .models import Booking

# Register your models here.

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'property',
        'tenant',
        'start_date',
        'end_date',
        'status',
        'booking_date'
    )

    search_fields = (
        'property__title',
        'tenant__username',
    )

    list_filter = (
        'status',
        'start_date',
        'end_date'
    )

    ordering = (
        '-booking_date',
    )
