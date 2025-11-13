from app.infrastructure.storage import StorageClient

class PresignService:
    """Service for generating presigned URLs."""

    def __init__(self, storage: StorageClient | None = None):
        self.storage = storage or StorageClient()

    def presign_url(self, key: str) -> str:
        """TODO: Delegate to storage client."""
        return self.storage.presign_url(key)
