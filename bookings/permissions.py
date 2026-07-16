from rest_framework.permissions import BasePermission


class IsBookingTenant(BasePermission):
    """
    Только пользователь, создавший бронь
    """

    def has_object_permission(self, request, view, obj):
        return obj.tenant == request.user



class IsPropertyOwner(BasePermission):
    """
    Владелец недвижимости
    """

    def has_object_permission(self, request, view, obj):
        return obj.property.owner == request.user
