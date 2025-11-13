from typing import Any
from sqlalchemy.orm import Session

class ProjectRepository:
    """Data access for projects."""

    def __init__(self, db: Session):
        self.db = db

    def list_projects(self) -> list[Any]:
        """TODO: Implement query."""
        raise NotImplementedError
