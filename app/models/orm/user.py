# app/models/orm/user.py
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean
from app.models.orm.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # TODO: tenant_id, roles, etc.
