from sqlalchemy.orm import Mapped, mapped_column
from app.models.orm.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO: add fields (username/email, tenant, etc.)
