from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db import get_db
from app.repositories.project_repository import ProjectRepository
from app.services.user_project_service import UserProjectService

def get_user_project_service(
    db: Session = Depends(get_db),
) -> UserProjectService:
    """Provide UserProjectService instance."""
    _repo = ProjectRepository(db=db)
    return UserProjectService()  # TODO: pass repo when service accepts it
