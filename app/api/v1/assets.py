from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_presign_service
from app.models.schemas.asset import PresignRequest, PresignResponse
from app.services.presign_service import PresignService

router = APIRouter()

@router.post(
    "/presign",
    response_model=PresignResponse,
    summary="Generate a presigned URL for uploading an asset",
)
async def presign_asset_upload(
    payload: PresignRequest,
    svc: PresignService = Depends(get_presign_service),
) -> PresignResponse:
    """Return a presigned upload URL for a dataset asset."""
    try:
        upload_url, object_key, bucket = svc.presign_upload(
            dataset_id=payload.dataset_id,
            filename=payload.filename,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return PresignResponse(upload_url=upload_url, object_key=object_key, bucket=bucket)
