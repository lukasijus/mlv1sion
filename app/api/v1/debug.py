# app/api/v1/debug.py
from fastapi import APIRouter, Depends
from app.core.config import settings

router = APIRouter()


@router.get("/env")
def debug_env():
    """Return the current environment settings for debugging purposes."""
    return {"environment": settings.env}
