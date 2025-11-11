# app/services/presign.py
from botocore.client import Config
import boto3
from app.config import settings
from datetime import timedelta

s3 = boto3.client(
    "s3",
    endpoint_url=f"http://{settings.MINIO_ENDPOINT}",
    aws_access_key_id=settings.MINIO_ACCESS_KEY,
    aws_secret_access_key=settings.MINIO_SECRET_KEY,
    config=Config(signature_version="s3v4"),
)


def generate_presigned_put(bucket: str, key: str, expires_seconds: int = 900):
    return s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_seconds,
        HttpMethod="PUT",
    )
