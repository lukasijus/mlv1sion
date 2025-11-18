# app/main.py
from fastapi import FastAPI
from app.api.v1.router import api_v1_router
from app.api import google_oauth


def create_app() -> FastAPI:
    app = FastAPI(title="mlv1sion API")
    # TODO: add middleware, exception handlers, etc.
    app.include_router(api_v1_router, prefix="/api/v1")
    app.include_router(google_oauth.router)
    return app


app = create_app()


@app.on_event("startup")
def create_demo_data():
    from app.infrastructure.db import SessionLocal
    from app.models.orm.project import Project
    from app.models.orm.dataset import Dataset

    db = SessionLocal()
    try:
        project = db.query(Project).first()
        if project is None:
            project = Project(
                name="Demo project",
                description="Automatically created",
            )
            db.add(project)
            db.commit()
            db.refresh(project)

        # only create datasets if none exist
        if not db.query(Dataset).filter(Dataset.project_id == project.id).first():
            db.add_all(
                [
                    Dataset(
                        project_id=project.id,
                        name="Demo dataset 1",
                        description="First demo dataset",
                    ),
                    Dataset(
                        project_id=project.id,
                        name="Demo dataset 2",
                        description="Second demo dataset",
                    ),
                ]
            )
            db.commit()
    finally:
        db.close()
