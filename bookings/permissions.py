from rest_framework.permissions import BasePermission


class IsTenant(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == 'tenant')


class IsBookingTenant(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.tenant == request.user


class IsPropertyOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.property.owner == request.user


class IsBookingOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.tenant == request.user
