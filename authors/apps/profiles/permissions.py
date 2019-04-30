from rest_framework import permissions


class IsGetOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method == 'GET':
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
