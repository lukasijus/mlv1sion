# app/api/v1/auth.py
from fastapi import APIRouter, Depends
from app.api.deps import get_auth_service
from app.models.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService
from app.core.context import get_user_context, UserContext

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    svc: AuthService = Depends(get_auth_service),
):
    return await svc.login(payload)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    refresh_token: str,
    svc: AuthService = Depends(get_auth_service),
):
    return await svc.refresh(refresh_token)


@router.get("/me")
async def me(ctx: UserContext = Depends(get_user_context)):
    return ctx
