from rest_framework import serializers

from moss.store import models
from moss.store.service import S3_SERVICE


class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = models.File
        fields = ("id", "name", "path", "created_at", "updated_at", "file")

    def create(self, validated_data):
        file = validated_data.pop("file")
        tenant = validated_data.pop("tenant")
        path = validated_data["path"]
        S3_SERVICE.upload_file(file, tenant, path)
        return super().create(validated_data)


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Permission
        fields = ("id", "user", "file", "role")
