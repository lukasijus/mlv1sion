from fastapi import APIRouter
from . import auth, projects, datasets, assets, jobs, debug

api_v1_router = APIRouter()
api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_v1_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_v1_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
api_v1_router.include_router(assets.router, prefix="/assets", tags=["assets"])
api_v1_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_v1_router.include_router(debug.router, prefix="/debug", tags=["debug"])
