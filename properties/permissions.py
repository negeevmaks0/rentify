from rest_framework.permissions import BasePermission, SAFE_METHODS



class IsLandlord(BasePermission):
    '''
    Только арендодатели
    '''

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == 'landlord'
        )



class IsTenant(BasePermission):
    '''
    Только арендаторы
    '''

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == 'tenant'
        )



class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user



class IsPropertyOwner(BasePermission):
    """
    Проверка владельца объявления через изображение
    """

    def has_object_permission(self, request, view, obj):
        return obj.property.owner == request.user
