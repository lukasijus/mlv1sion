from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
async def login():
    """TODO: Authenticate user and return tokens."""
    raise NotImplementedError

@router.post("/refresh")
async def refresh():
    """TODO: Refresh access token."""
    raise NotImplementedError

@router.get("/me")
async def me():
    """TODO: Return current user info."""
    raise NotImplementedError
