from app.infrastructure.storage import StorageClient
from app.repositories.dataset_repository import DatasetRepository


class PresignService:
    """Service for generating presigned URLs."""

    def __init__(
        self,
        storage: StorageClient,
        dataset_repo: DatasetRepository,
    ):
        self.storage = storage
        self.dataset_repo = dataset_repo

    def presign_upload(self, dataset_id: int, filename: str) -> tuple[str, str, str]:
        """Return a presigned URL, key, and bucket for uploading an asset into a dataset."""
        dataset = self.dataset_repo.get(dataset_id)
        if dataset is None:
            raise ValueError(f"Dataset {dataset_id} not found")

        key = f"datasets/{dataset.id}/{filename}"
        url = self.storage.presign_url(key)
        return url, key, self.storage.bucket
