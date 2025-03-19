from django.contrib.auth.models import AbstractUser
from django.db import models


class Tenant(models.Model):
    """An organization or account with multiple users"""

    # TODO: Practically, we want an internal, strictly unique
    # identifier and a not-so-strict display name. But
    # for right now, name will serve.
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Extend Django's built-in User to connect tenant"""

    REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ["tenant_id"]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)


class File(models.Model):
    """Metadata that connects S3 objects to our concept of files"""

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=1024)
    s3_key = models.CharField(max_length=1024)
    size = models.BigIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tenant}/{self.path}/{self.name}"


class Permission(models.Model):
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("EDITOR", "Editor"),
        ("VIEWER", "Viewer"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
