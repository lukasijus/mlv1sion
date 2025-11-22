# app/services/user_dataset_service.py
from collections.abc import Sequence
from typing import Any

from app.models.orm.dataset import Dataset
from app.models.schemas.dataset import DatasetCreate
from app.repositories.dataset_repository import DatasetRepository


class UserDatasetService:
    """User-aware dataset service (per-user/tenant rules live here)."""

    def __init__(self, dataset_repo: DatasetRepository):
        self._repo = dataset_repo

    def list_datasets_for_user(
        self,
        project_id: int,
        user: Any | None = None,  # later: real user type
    ) -> Sequence[Dataset]:
        # TODO: enforce user/tenant access based on `user`
        return self._repo.list_by_project(project_id=project_id)

    def create_dataset_for_user(
        self,
        payload: DatasetCreate,
        user: Any | None = None,
    ) -> Dataset:
        # TODO: enforce user/tenant access based on `user`
        return self._repo.create(
            project_id=payload.project_id,
            name=payload.name,
            description=payload.description,
        )
