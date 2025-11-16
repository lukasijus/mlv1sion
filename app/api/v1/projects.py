# app/api/v1/projects.py
from typing import Sequence

from fastapi import APIRouter, Depends

from app.api.deps import get_user_project_service
from app.models.schemas.project import ProjectRead
from app.services.user_project_service import UserProjectService


router = APIRouter()


@router.get(
    "/", response_model=list[ProjectRead], summary="List projects for the current user"
)
async def list_projects(
    svc: UserProjectService = Depends(get_user_project_service),
) -> Sequence[ProjectRead]:
    """List projects for the current user/tenant."""
    projects = svc.list_projects_for_user(user=None)  # TODO: wire current user
    return projects
