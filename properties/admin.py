from django.contrib import admin

from .models import Property, PropertyImage

# Register your models here.

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'owner',
        'price_per_month',
        'property_type',
        'room_count',
        'is_active',
        'created_at'
    )

    search_fields = (
        'title',
        'description',
        'location'
    )

    list_filter = (
        'property_type',
        'is_active',
        'created_at'
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = ('created_at',)

    list_per_page = 20



@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = (
        'property',
        'image'
    )

    search_fields = (
        'property__title',
    )
