# app/api/v1/projects.py
from typing import Sequence

from fastapi import APIRouter, Depends, status

from app.api.deps import get_user_project_service
from app.models.schemas.project import ProjectCreate, ProjectRead
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


@router.post(
    "/",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a project",
)
async def create_project(
    payload: ProjectCreate,
    svc: UserProjectService = Depends(get_user_project_service),
) -> ProjectRead:
    """Create a project for the current user/tenant."""
    project = svc.create_project(payload=payload, user=None)  # TODO: wire current user
    return project
