from collections.abc import Sequence
from typing import Any

from sqlalchemy.orm import Session

from app.models.orm.project import Project


class ProjectRepository:
    """Data access for projects."""

    def __init__(self, db: Session):
        self.db = db

    def list_projects(self) -> Sequence[Project]:
        """TODO: Implement filters (tenant, user) later."""
        return self.db.query(Project).all()
