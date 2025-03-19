from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from moss.store.models import File
from moss.store.perms import HasFilePermission
from moss.store.serializers import FileSerializer, PermissionSerializer


class FileViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing file operations in multi-tenant S3 storage.

    Provides endpoints for listing, retrieving, creating, updating, and deleting files,
    as well as specialized actions for upload and download operations.
    """

    serializer_class = FileSerializer
    permission_classes = (IsAuthenticated, HasFilePermission)

    def get_queryset(self):
        """Return only files belonging to the current user's tenant."""
        return File.objects.filter(tenant=self.request.user.tenant)

    # Custom actions for upload/download
    @action(detail=False, methods=["post"])
    def upload(self, _request):
        """
        Upload a file to S3 storage.

        The file will be associated with the current user's tenant and
        stored with appropriate permissions.
        """

    @action(detail=True, methods=["get"])
    def download(self, _request, _pk=None):
        """
        Generate a pre-signed URL for downloading the file.

        The URL is temporary and will expire after a configured time period.
        """


class PermissionViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing file permissions in the multi-tenant storage system.

    Provides endpoints for listing, creating, updating, and removing permissions
    for users to access files. Only administrators can modify permissions.

    Permissions define what actions (view, edit, admin) a user can perform on a file.
    """

    serializer_class = PermissionSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
