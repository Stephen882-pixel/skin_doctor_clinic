from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object or admins to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Allow admin users full access
        if request.user.is_staff:
            return True
        
        # Check if the object has a user attribute (like Doctor or Patient models)
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Object is a User model itself
        return obj == request.user


class IsAdminUser(permissions.BasePermission):
    """
    Permission to only allow admin users to access.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_staff