from collections.abc import Generator
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from app.core.config import settings
from app.models.orm.base import Base
from app.models.orm import project  # noqa: F401  # register model
from app.models.orm import dataset  # noqa: F401  # register model

engine = create_engine(settings.database_url, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# DEV ONLY: auto-create tables until Alembic is set up
Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
