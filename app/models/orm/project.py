from sqlalchemy.orm import Mapped, mapped_column
from app.models.orm.base import Base

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO: add fields (name, description, timestamps, etc.)
