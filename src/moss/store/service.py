import boto3
from django.conf import settings


class S3Service:
    def __init__(self):
        self.s3_client = boto3.client("s3")
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def generate_key(self, tenant_id, file_path):
        return f"{tenant_id}/{file_path}"

    def upload_file(self, file_obj, tenant_id, file_path):
        key = self.generate_key(tenant_id, file_path)
        self.s3_client.upload_fileobj(file_obj, self.bucket_name, key)
        return key

    def generate_presigned_url(self, key, expiration_secs=3600):
        params = (
            {
                "Bucket": self.bucket_name,
                "Key": key,
            },
        )
        return self.s3_client.generate_presigned_url("get_object", Params=params, ExpiresIn=expiration_secs)
