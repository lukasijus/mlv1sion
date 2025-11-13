from sqlalchemy.orm import Mapped, mapped_column
from app.models.orm.base import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO: add fields (project_id, name, etc.)
