from collections.abc import Sequence
from typing import Any

from app.models.orm.project import Project
from app.repositories.project_repository import ProjectRepository


class UserProjectService:
    """Business logic for users, tenants, projects, memberships."""

    def __init__(self, project_repo: ProjectRepository):
        self._project_repo = project_repo

    def list_projects_for_user(self, user: Any | None = None) -> Sequence[Project]:
        """TODO: filter by user/tenant once auth is wired."""
        return self._project_repo.list_projects()
