from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.db import get_db
from app.repositories.project_repository import ProjectRepository
from app.services.user_project_service import UserProjectService


def get_user_project_service(
    db: Session = Depends(get_db),
) -> UserProjectService:
    """Provide UserProjectService instance."""
    repo = ProjectRepository(db=db)
    return UserProjectService(project_repo=repo)
