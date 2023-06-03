from django.utils.translation import gettext_lazy as _
from rest_framework import permissions


class IsSuperUserAccessPermission(permissions.BasePermission):
    message = _('Customers not allowed.')

    def has_permission(self, request, view):
        user = request.user
        return user.is_superuser


class AllowOwner(permissions.IsAuthenticated):
    message = _('You are not the owner.')

    def has_object_permission(self, request, view, obj):
        if not (request.user and request.user.is_authenticated):
            return False

        user = request.user
        if obj.user_id == user.pk:
            return True
        return False


class AllowStaff(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        return request.user.is_staff
        # user_info = request.user_info
        # return user_info.is_staff


class AllowStaffOrOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        # user_info = request.user_info
        # if obj.user_id == user.pk or user_info.is_staff:
        if obj.user_id == user.pk or user.is_staff:
            return True
        return False
