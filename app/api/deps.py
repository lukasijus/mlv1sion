# app/api/deps.py
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.db import get_db
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.dataset_repository import DatasetRepository
from app.services.presign_service import PresignService
from app.infrastructure.storage import StorageClient
from app.services.user_project_service import UserProjectService
from app.services.user_dataset_service import UserDatasetService


def get_auth_service(
    db: Session = Depends(get_db),
) -> AuthService:
    """Provide AuthService instance."""
    repo = UserRepository(db=db)
    return AuthService(user_repo=repo)


def get_user_project_service(
    db: Session = Depends(get_db),
) -> UserProjectService:
    """Provide UserProjectService instance."""
    repo = ProjectRepository(db=db)
    return UserProjectService(project_repo=repo)


def get_user_dataset_service(
    db: Session = Depends(get_db),
) -> UserDatasetService:
    """Provide UserDatasetService instance."""
    repo = DatasetRepository(db=db)
    return UserDatasetService(dataset_repo=repo)


def get_presign_service(
    db: Session = Depends(get_db),
) -> PresignService:
    """Provide PresignService instance."""
    dataset_repo = DatasetRepository(db=db)
    try:
        storage = StorageClient()
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    return PresignService(storage=storage, dataset_repo=dataset_repo)
