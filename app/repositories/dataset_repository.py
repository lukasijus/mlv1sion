from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.orm.dataset import Dataset


class DatasetRepository:
    """Data access for datasets."""

    def __init__(self, db: Session):
        self.db = db

    def list_by_project(self, project_id: int) -> Sequence[Dataset]:
        """Return datasets for a given project."""
        return (
            self.db.query(Dataset)
            .filter(Dataset.project_id == project_id)
            .order_by(Dataset.id)
            .all()
        )
