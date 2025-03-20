import boto3
from django.conf import settings


class S3Service:
    def __init__(self):
        self.s3_client = boto3.client("s3")
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def generate_key(self, tenant_id, file_path, file_name):
        """Generate the per-tenant prefix path for a file"""
        return f"{tenant_id}/{file_path}/{file_name}"

    def upload_file(self, file_obj, tenant_id, file_path, file_name):
        """Upload a file to s3 and return the file's metadata"""
        # TODO make this async?
        key = self.generate_key(tenant_id, file_path, file_name)
        self.s3_client.upload_fileobj(file_obj, self.bucket_name, key)
        # self.s3_client.Object(self.bucket_name, key).wait_until_exists()
        return key

    def generate_presigned_url(self, key, expiration_secs=3600):
        """In lieu of actually downloading, for now"""
        params = {
            "Bucket": self.bucket_name,
            "Key": key,
        }
        return self.s3_client.generate_presigned_url("get_object", Params=params, ExpiresIn=expiration_secs)


S3_SERVICE = S3Service()
