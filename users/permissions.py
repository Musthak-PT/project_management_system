from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.role == 'manager'

class IsMember(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.role == 'manager' or request.user.role == 'member'