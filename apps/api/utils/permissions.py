from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.is_staff:
                return True
            return request.user == obj.user


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return True if request.method in permissions.SAFE_METHODS else request.user.is_staff

