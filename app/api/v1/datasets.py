from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_datasets():
    """TODO: List datasets for a project."""
    raise NotImplementedError
