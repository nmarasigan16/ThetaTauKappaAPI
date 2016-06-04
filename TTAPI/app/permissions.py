from rest_framework import permissions

class IsOfficer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated():
            if request.method == 'DELETE':
                return request.user.is_staff
            return request.user.has_perm('app.officer')
        else:
            return False
