import boto3, os
from ..core.config import settings

def get_s3():
    s3 = boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        region_name=settings.S3_REGION,
        use_ssl=settings.S3_USE_SSL,
    )
    return s3

def ensure_bucket():
    s3 = get_s3()
    buckets = [b["Name"] for b in s3.list_buckets().get("Buckets", [])]
    if settings.S3_BUCKET not in buckets:
        s3.create_bucket(Bucket=settings.S3_BUCKET)
    return True
