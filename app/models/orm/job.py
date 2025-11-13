from sqlalchemy.orm import Mapped, mapped_column
from app.models.orm.base import Base

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO: add fields (type, status, timestamps, etc.)
