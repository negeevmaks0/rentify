from rest_framework.permissions import BasePermission



class IsLandlord(BasePermission):
    '''
    Только арендодатели
    '''

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'landlord'
        )



class IsTenant(BasePermission):
    '''
    Только арендаторы
    '''

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'tenant'
        )