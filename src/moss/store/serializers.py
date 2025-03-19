from rest_framework import serializers

from moss.store import models


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = ("id", "name", "path", "size", "created_at", "updated_at")


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Permission
        fields = ("id", "user", "file", "role")
