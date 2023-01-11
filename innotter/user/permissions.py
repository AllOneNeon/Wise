from rest_framework import permissions

from .models import User

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role:
            return request.user.role == User.Roles.ADMIN
        return False

class IsUserOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user

class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Roles.MODERATOR
