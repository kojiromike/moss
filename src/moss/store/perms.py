from rest_framework.permissions import SAFE_METHODS, BasePermission

from moss.store.models import Permission


class HasFilePermission(BasePermission):
    """Determine if the request context has permission to interact with the file according to the request method."""

    def has_object_permission(self, request, _view, obj):
        # Check if user has permission for this file
        # SAFE_METHODS are defined in rest_framework as essentially reader methods
        if request.method in SAFE_METHODS:
            # Check for viewer permission
            return Permission.objects.filter(
                user=request.user, file=obj, role__in=("VIEWER", "EDITOR", "ADMIN")
            ).exists()
        # Check for editor permission
        return Permission.objects.filter(user=request.user, file=obj, role__in=("EDITOR", "ADMIN")).exists()
