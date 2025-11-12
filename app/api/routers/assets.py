# app/api/routers/assets.py
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from enum import StrEnum
from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Header, Query, status
from pydantic import BaseModel, Field

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.rbac import require_roles, get_current_token
from app.db.sessions import get_db
from app.models import orm
from app.services.presign import generate_presigned_put
from app.config import settings

import boto3
from botocore.client import Config as BotoConfig
import botocore.exceptions

router = APIRouter()

# --- S3 client (blocking but fine for short HEAD/PUT signing) ---
_s3 = boto3.client(
    "s3",
    endpoint_url=f"http://{settings.MINIO_ENDPOINT}",
    aws_access_key_id=settings.MINIO_ACCESS_KEY,
    aws_secret_access_key=settings.MINIO_SECRET_KEY,
    config=BotoConfig(signature_version="s3v4"),
)

# ========= Schemas =========


class AssetStatus(StrEnum):
    CREATED = "CREATED"
    UPLOADING = "UPLOADING"
    READY = "READY"
    DELETING = "DELETING"
    DELETED = "DELETED"


class AssetOut(BaseModel):
    id: str
    tenant_id: str
    key: str
    sha256: Optional[str] = None
    size: Optional[int] = None
    status: AssetStatus
    created_at: datetime

    class Config:
        from_attributes = True


class InitiateUploadIn(BaseModel):
    filename: str = Field(
        ..., description="Original filename (used to hint content-type)"
    )
    content_type: Optional[str] = Field(None, description="MIME type if known")
    size_hint: Optional[int] = Field(None, description="Client-reported size; advisory")


class InitiateUploadOut(BaseModel):
    asset_id: str
    bucket: str
    key: str
    upload_url: str
    expires_at: datetime


class FinalizeUploadIn(BaseModel):
    asset_id: str
    key: str
    size: Optional[int] = None
    sha256: Optional[str] = None


class DeleteOut(BaseModel):
    asset_id: str
    status: AssetStatus


# ========= Helpers =========


def _tenant_bucket() -> str:
    # Simple: single bucket per deployment.
    # Per-tenant buckets, switch to: return f"{settings.BUCKET_PREFIX}-{tenant_id}"
    return "assets"


def _tenant_key_prefix(tenant_id: str) -> str:
    return f"tenants/{tenant_id}/assets/"


def _build_object_key(tenant_id: str, filename: str) -> str:
    safe_name = filename.replace("/", "_")
    return f"{_tenant_key_prefix(tenant_id)}{uuid4()}_{safe_name}"


# ========= Routes =========


@router.post(
    "/initiate",
    response_model=InitiateUploadOut,
    summary="Initiate direct-to-S3 upload (presigned PUT)",
    dependencies=[Depends(require_roles(["admin", "uploader"]))],
)
async def initiate_upload(
    payload: InitiateUploadIn,
    db: AsyncSession = Depends(get_db),
    token=Depends(get_current_token),
):
    tenant_id: str = token["tenant_id"]
    key = _build_object_key(tenant_id, payload.filename)
    bucket = _tenant_bucket()

    # Create asset row in CREATED/UPLOADING
    asset = await AssetRepo.create(
        db,
        tenant_id=tenant_id,
        key=key,
        status=AssetStatus.UPLOADING.value,
        size=payload.size_hint,
        sha256=None,
    )

    # Generate presigned URL (PUT)
    expires = timedelta(minutes=15)
    upload_url = generate_presigned_put(
        bucket=bucket, key=key, expires_seconds=int(expires.total_seconds())
    )
    return InitiateUploadOut(
        asset_id=asset.id,
        bucket=bucket,
        key=key,
        upload_url=upload_url,
        expires_at=datetime.now(timezone.utc) + expires,
    )


@router.post(
    "/finalize",
    response_model=AssetOut,
    summary="Finalize upload after client PUTs to S3",
    dependencies=[Depends(require_roles(["admin", "uploader"]))],
)
async def finalize_upload(
    payload: FinalizeUploadIn,
    db: AsyncSession = Depends(get_db),
    token=Depends(get_current_token),
    x_idempotency_key: Optional[str] = Header(default=None, alias="Idempotency-Key"),
):
    tenant_id: str = token["tenant_id"]

    # Fetch asset and validate tenant ownership
    asset = await AssetRepo.get_by_id_for_tenant(
        db, asset_id=payload.asset_id, tenant_id=tenant_id
    )
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    # Verify key matches (prevents spoofing finalize onto a different object)
    if asset.key != payload.key:
        raise HTTPException(status_code=400, detail="Key mismatch for asset")

    # HEAD the object in MinIO to confirm presence, size, and ETag
    try:
        meta = _s3.head_object(Bucket=_tenant_bucket(), Key=payload.key)
    except botocore.exceptions.ClientError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Object not found in storage: {e.response.get('Error', {}).get('Message', '')}",
        )

    content_len = int(meta.get("ContentLength", 0))
    etag = meta.get("ETag", "").strip('"')

    if payload.size is not None and payload.size != content_len:
        raise HTTPException(
            status_code=400,
            detail=f"Size mismatch (reported {payload.size}, stored {content_len})",
        )

    # NOTE: For single-part uploads, ETag == md5. For multipart, ETag != md5.
    # We accept client-provided sha256 as metadata; actual validation can be async.
    updated = await AssetRepo.mark_ready(
        db,
        asset_id=asset.id,
        size=content_len,
        sha256=payload.sha256,
    )
    return AssetOut.model_validate(updated)


@router.get(
    "",
    response_model=List[AssetOut],
    summary="List assets (tenant-scoped)",
    dependencies=[Depends(require_roles(["admin", "viewer", "uploader"]))],
)
async def list_assets(
    db: AsyncSession = Depends(get_db),
    token=Depends(get_current_token),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    tenant_id: str = token["tenant_id"]
    rows = await AssetRepo.list_for_tenant(
        db, tenant_id=tenant_id, limit=limit, offset=offset
    )
    return [AssetOut.model_validate(r) for r in rows]


@router.get(
    "/{asset_id}",
    response_model=AssetOut,
    summary="Get single asset (tenant-scoped)",
    dependencies=[Depends(require_roles(["admin", "viewer", "uploader"]))],
)
async def get_asset(
    asset_id: str,
    db: AsyncSession = Depends(get_db),
    token=Depends(get_current_token),
):
    tenant_id: str = token["tenant_id"]
    asset = await AssetRepo.get_by_id_for_tenant(
        db, asset_id=asset_id, tenant_id=tenant_id
    )
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return AssetOut.model_validate(asset)


@router.delete(
    "/{asset_id}",
    response_model=DeleteOut,
    summary="Soft-delete asset (mark DELETING; background cleanup)",
    dependencies=[Depends(require_roles(["admin"]))],
)
async def delete_asset(
    asset_id: str,
    db: AsyncSession = Depends(get_db),
    token=Depends(get_current_token),
):
    tenant_id: str = token["tenant_id"]
    asset = await AssetRepo.get_by_id_for_tenant(
        db, asset_id=asset_id, tenant_id=tenant_id
    )
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    await AssetRepo.mark_deleting(db, asset_id=asset_id)

    # Enqueue background deletion of the object and final tombstone (outbox/event)
    # (Implement a Celery task that deletes S3 object and then mark DELETED)
    # celery_app.send_task("app.tasks.assets.delete_object", args=[asset_id])

    return DeleteOut(asset_id=asset_id, status=AssetStatus.DELETING)
