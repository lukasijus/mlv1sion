# app/services/auth_service.py
from typing import Any

from fastapi import HTTPException, status

from app.core.security import (
    AuthUser,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from app.models.schemas.auth import LoginRequest, TokenResponse
from app.repositories.user_repository import UserRepository


class AuthService:
    """Authentication and token management service."""

    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    async def login(self, payload: LoginRequest) -> TokenResponse:
        user = self._user_repo.get_by_email(payload.email)

        if not user or not verify_password(payload.password, user.password_hash):
            # For now we let service throw HTTPException;
            # later you can refactor to domain errors.
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # TODO: load tenant_id, roles, permissions from user/joins
        auth = AuthUser(
            id=user.id,
            tenant_id=None,
            roles=(),
            permissions=(),
        )

        access = create_access_token(auth)
        refresh = create_refresh_token(auth)

        return TokenResponse(
            access_token=access,
            refresh_token=refresh,
        )

    async def refresh(self, refresh_token: str) -> TokenResponse:
        from app.core.security import decode_token  # avoid cycle at top-level

        auth = decode_token(refresh_token, expected_type="refresh")

        access = create_access_token(auth)
        new_refresh = create_refresh_token(auth)

        return TokenResponse(
            access_token=access,
            refresh_token=new_refresh,
        )
