# app/repositories/user_repository.py
from typing import Optional

from sqlalchemy.orm import Session

from app.models.orm.user import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_email(self, email: str) -> Optional[User]:
        return self._db.query(User).filter(User.email == email).first()

    def get_by_google_id(self, google_id: str) -> Optional[User]:
        return self._db.query(User).filter(User.google_id == google_id).first()

    def create(
        self,
        email: str,
        password_hash: str | None = None,
        google_id: str | None = None,
    ) -> User:
        user = User(email=email, password_hash=password_hash, google_id=google_id)
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def link_google_account(self, user: User, google_id: str) -> User:
        user.google_id = google_id
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user
