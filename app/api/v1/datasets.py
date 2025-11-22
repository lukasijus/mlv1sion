# app/api/v1/datasets.py
from typing import Sequence

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_user_dataset_service
from app.models.schemas.dataset import DatasetCreate, DatasetRead
from app.services.user_dataset_service import UserDatasetService

router = APIRouter()


@router.get(
    "/",
    response_model=list[DatasetRead],
    summary="List datasets for a project",
)
async def list_datasets(
    project_id: int = Query(..., description="Project ID"),
    svc: UserDatasetService = Depends(get_user_dataset_service),
) -> Sequence[DatasetRead]:
    """List datasets belonging to the given project."""
    return svc.list_datasets_for_user(project_id=project_id)


@router.post(
    "/",
    response_model=DatasetRead,
    status_code=201,
    summary="Create dataset",
)
async def create_dataset(
    payload: DatasetCreate,
    svc: UserDatasetService = Depends(get_user_dataset_service),
) -> DatasetRead:
    """Create a dataset under a project."""
    return svc.create_dataset_for_user(payload)
