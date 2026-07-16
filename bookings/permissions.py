from rest_framework.permissions import BasePermission



class IsTenant(BasePermission):
    """
    Только арендаторы
    """

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == 'tenant')



class IsBookingTenant(BasePermission):
    """
    Только пользователь, создавший бронь
    """

    def has_object_permission(self, request, view, obj):
        return obj.tenant == request.user



class IsPropertyOwnerForBooking(BasePermission):
    """
    Владелец недвижимости
    """

    def has_object_permission(self, request, view, obj):
        return obj.property.owner == request.user
