from io import StringIO

import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from moss.store.jwt import get_tokens_for_user
from moss.store.models import Tenant, User

# ./manage.py show_urls | grep file
# /api/v1/files/	moss.store.views.FileViewSet	file-list
# /api/v1/files/<int:id>/	moss.store.views.FileViewSet
# /api/v1/files/<pk>/	moss.store.views.FileViewSet	file-detail
# /api/v1/files/<pk>/download/	moss.store.views.FileViewSet	file-download
# /api/v1/files/<pk>/download\.<format>/	moss.store.views.FileViewSet	file-download
# /api/v1/files/<pk>\.<format>/	moss.store.views.FileViewSet	file-detail
# /api/v1/files/upload/	moss.store.views.FileViewSet	file-upload
# /api/v1/files/upload\.<format>/	moss.store.views.FileViewSet	file-upload
# /api/v1/files\.<format>/	moss.store.views.FileViewSet	file-list


class AdminFileOpsTests(TestCase):
    """Test that we meet the requirements for the file API. That is:

    - Users can upload, manage, and access files
    - Not all users are able to upload, manage, or access all files
    - Files are stored in a cloud storage service
    - Files are accessible to user-managed processes with the right credentials.
    - Aptible's systems can manage customer storage at all times
    """

    def setUp(self):
        tenant = Tenant.objects.create(name="test_tenant")
        user = User.objects.create_user(username="test_user", email="ex@example.com", password="hunter2", tenant=tenant)
        user.save()
        tokens = get_tokens_for_user(user)
        self.tenant_id = tenant.id
        self.api_client = APIClient()
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")

    def test_list_files(self):
        """An Aptible user can list all files."""
        url = reverse("file-list")
        response = self.api_client.get(url, {"path": "some/path", "tenant": self.tenant_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_file(self):
        """An Aptible user can upload a file anywhere."""
        url = reverse("file-upload")
        with StringIO() as example:
            response = self.api_client.post(url, {"file": example, "path": "some/path", "tenant": self.tenant_id})
        assert response.status_code == status.HTTP_201_CREATED

    def test_download_file(self):
        """An Aptible user can download any file."""
        url = reverse("file-download", args=[1])
        response = self.api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
