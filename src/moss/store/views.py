from resetframework.decorators import action
from restframework import viewsets
from restframework.permissions import IsAdminUser, IsAuthenticated

from moss.store.models import File
from moss.store.perms import HasFilePermission
from moss.store.serializers import FileSerializer, PermissionSerializer


class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    permission_classes = (IsAuthenticated, HasFilePermission)

    def get_queryset(self):
        return File.objects.filter(tenant=self.request.user.tenant)

    # Custom actions for upload/download
    @action(detail=False, methods=["post"])
    def upload(self, request):
        # Handle file upload to S3
        pass

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        # Generate presigned URL for download
        pass


class PermissionViewSet(viewsets.ModelViewSet):
    serializer_class = PermissionSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
