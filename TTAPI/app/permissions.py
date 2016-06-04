from rest_framework import permissions

class IsOfficer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated():
            if request.method == 'DELETE':
                return request.user.is_staff
            return request.user.has_perm('app.officer')
        else:
            return False

class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated():
            if request.method in permissions.SAFE_METHODS:
                return True
        return False

#not exactly what it sounds like
class IsPledge(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.profile.demographics.status == 'P':
            return True

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.profile.pledge == obj.pledge
