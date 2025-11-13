from typing import Any
from sqlalchemy.orm import Session

class JobRepository:
    """Data access for jobs."""

    def __init__(self, db: Session):
        self.db = db

    def list_jobs(self) -> list[Any]:
        """TODO: Implement query."""
        raise NotImplementedError
