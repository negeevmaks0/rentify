from django.contrib import admin

from .models import \
    User, \
    Property, PropertyImage, \
    Booking, Review



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



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'property',
        'author',
        'rating',
        'created_at'
    )

    search_fields = (
        'property__title',
        'author__username',
        'comment'
    )

    list_filter = (
        'rating',
        'created_at'
    )



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'is_active'
    )

    search_fields = (
        'username',
        'email'
    )

    list_filter = (
        'role',
        'is_active'
    )
