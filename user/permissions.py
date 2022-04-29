from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    DRF Permission class to check if user is admin
    """
    message = 'You must be an admin to access this API.'

    def has_permission(self, request, view):
        return request.user.is_superuser

