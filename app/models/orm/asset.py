from sqlalchemy.orm import Mapped, mapped_column
from app.models.orm.base import Base

class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO: add fields (dataset_id, filename, status, etc.)
