from __future__ import annotations

from typing import Final
from urllib.parse import urlparse

import boto3
from botocore.config import Config

from app.core.config import settings


class StorageClient:
    """S3-compatible storage client backed by MinIO."""

    def __init__(
        self,
        endpoint: str | None = None,
        access_key: str | None = None,
        secret_key: str | None = None,
        bucket: str | None = None,
        region: str | None = None,
        use_ssl: bool | None = None,
    ):
        self.endpoint: Final[str | None] = endpoint or settings.minio_endpoint
        self.access_key: Final[str | None] = access_key or settings.minio_access_key
        self.secret_key: Final[str | None] = secret_key or settings.minio_secret_key
        self.bucket: Final[str | None] = bucket or settings.minio_bucket
        self.region: Final[str] = region or settings.minio_region
        self.use_ssl: Final[bool] = bool(settings.minio_use_ssl if use_ssl is None else use_ssl)

        missing = [
            name
            for name, value in {
                "minio_endpoint": self.endpoint,
                "minio_access_key": self.access_key,
                "minio_secret_key": self.secret_key,
                "minio_bucket": self.bucket,
            }.items()
            if not value
        ]
        if missing:
            joined = ", ".join(missing)
            raise ValueError(f"Storage configuration is incomplete; missing: {joined}")

        self._client = boto3.client(
            "s3",
            endpoint_url=self._build_endpoint_url(self.endpoint, self.use_ssl),
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region,
            config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
            use_ssl=self.use_ssl,
        )

    def presign_url(self, key: str, expires_in: int = 3600) -> str:
        """Return a presigned PUT URL for uploading an object."""
        if not key:
            raise ValueError("Object key must be provided.")
        return self._client.generate_presigned_url(
            ClientMethod="put_object",
            Params={"Bucket": self.bucket, "Key": key},
            ExpiresIn=expires_in,
        )

    @staticmethod
    def _build_endpoint_url(endpoint: str, use_ssl: bool) -> str:
        """Ensure endpoint has scheme."""
        parsed = urlparse(endpoint)
        if parsed.scheme:
            return endpoint
        scheme = "https" if use_ssl else "http"
        return f"{scheme}://{endpoint}"
