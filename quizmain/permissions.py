from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    The request is admin user, or is a read-only request.
    """    
    def has_permission(self, request, view):
        
        return bool(request.method in SAFE_METHODS or request.user.is_staff)

class IsAdminOrIsOwner(BasePermission):
    """
    The request is admin user, or is a read-only request.
    """    
    def has_object_permission(self, request, view, obj):
        
        return bool(obj.user_id == request.user or request.user.is_staff)