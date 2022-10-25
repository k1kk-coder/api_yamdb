from rest_framework import permissions


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == 'admin'
            or request.user.is_staff
        )


class AdminOrGetRequestPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'


class AuthorOrStaffPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            obj.author == request.user or request.user.role == 'admin'
            or request.user.role == 'moderator' or request.user.is_staff
        )
