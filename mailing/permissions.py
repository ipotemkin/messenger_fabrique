from rest_framework import permissions

from users.managers import UserRoles


class IsAdmin(permissions.BasePermission):
    message = 'Allowed only for admins'

    def has_permission(self, request, view):
        return request.user.role == UserRoles.ADMIN
