from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_assets():
    """TODO: List assets for a dataset."""
    raise NotImplementedError
