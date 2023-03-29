from rest_framework import permissions
from apps.records.models.user import Role


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.role == Role.STUDENT


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.role == Role.TEACHER


class IsSecretary(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.role == Role.SECRETARY


class ModelPermissions(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


def user_has_perms(perms):
    class _Permission(permissions.BasePermission):
        _perms = perms

        def has_permission(self, request, view):
            if not (request.user and request.user.is_authenticated):
                return False
            return request.user.has_perms(self._perms)

    return _Permission
