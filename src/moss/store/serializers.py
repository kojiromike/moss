from rest_framework import serializers

from moss.store import models
from moss.store.service import S3_SERVICE


class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = models.File
        fields = ("id", "name", "path", "created_at", "updated_at", "file", "created_by")

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        tenant = request.user.tenant
        created_by = user
        file = validated_data.pop("file")
        path = validated_data["path"]
        name = validated_data["name"]
        validated_data["tenant"] = tenant
        validated_data["created_by"] = created_by
        S3_SERVICE.upload_file(file, tenant, path, name)
        return super().create(validated_data)


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Permission
        fields = ("id", "user", "file", "role")
