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

    def get(self, dataset_id: int) -> Dataset | None:
        """Fetch a dataset by id."""
        return self.db.query(Dataset).filter(Dataset.id == dataset_id).one_or_none()

    def create(self, project_id: int, name: str, description: str | None = None) -> Dataset:
        """Create and persist a dataset."""
        dataset = Dataset(project_id=project_id, name=name, description=description)
        self.db.add(dataset)
        self.db.commit()
        self.db.refresh(dataset)
        return dataset
