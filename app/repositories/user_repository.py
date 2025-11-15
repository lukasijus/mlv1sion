# app/repositories/user_repository.py
from typing import Optional

from sqlalchemy.orm import Session

from app.models.orm.user import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_email(self, email: str) -> Optional[User]:
        return self._db.query(User).filter(User.email == email).first()
