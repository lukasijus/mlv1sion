# app/api/deps.py
from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.db import get_db
from app.repositories.project_repository import ProjectRepository
from app.repositories.dataset_repository import DatasetRepository
from app.services.user_project_service import UserProjectService
from app.services.user_dataset_service import UserDatasetService


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
