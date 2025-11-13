from typing import Any
from sqlalchemy.orm import Session

class UserRepository:
    """Data access for users."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Any:
        """TODO: Implement query."""
        raise NotImplementedError
