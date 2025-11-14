from fastapi import FastAPI
from app.api.v1.router import api_v1_router


def create_app() -> FastAPI:
    app = FastAPI(title="mlv1sion API")
    # TODO: add middleware, exception handlers, etc.
    app.include_router(api_v1_router, prefix="/api/v1")
    return app


app = create_app()


@app.on_event("startup")
def create_demo_data():
    from app.infrastructure.db import SessionLocal
    from app.models.orm.project import Project

    db = SessionLocal()
    if not db.query(Project).first():
        db.add(Project(name="Demo project", description="Automatically created"))
        db.commit()
    db.close()
