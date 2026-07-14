from django.contrib import admin

from .models import Review

# Register your models here.

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'booking',
        'author',
        'rating',
        'created_at'
    )

    search_fields = (
        'booking__property__title',
        'author__username',
        'comment'
    )

    list_filter = (
        'rating',
        'created_at'
    )
