# app/services/auth_service.py
from __future__ import annotations

from datetime import datetime, timedelta
import secrets
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import httpx
from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.core.config import settings
from app.core.security import (
    AuthUser,
    verify_password,
    hash_password,
    create_access_token,
    create_refresh_token,
)
from app.models.orm.user import User
from app.models.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.repositories.user_repository import UserRepository

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"
DEFAULT_GOOGLE_FRONTEND_REDIRECT = "/auth/google/callback"
GOOGLE_STATE_TYPE = "google_oauth_state"


class AuthService:
    """Authentication and token management service."""

    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    async def register(self, payload: RegisterRequest) -> TokenResponse:
        existing_user = self._user_repo.get_by_email(payload.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        password_hash = hash_password(payload.password)
        user = self._user_repo.create(
            email=payload.email,
            password_hash=password_hash,
        )
        return self._issue_tokens(user)

    async def login(self, payload: LoginRequest) -> TokenResponse:
        user = self._user_repo.get_by_email(payload.email)

        if (
            not user
            or not user.password_hash
            or not verify_password(payload.password, user.password_hash)
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        return self._issue_tokens(user)

    async def refresh(self, refresh_token: str) -> TokenResponse:
        from app.core.security import decode_token  # avoid cycle at top-level

        auth = decode_token(refresh_token, expected_type="refresh")

        access = create_access_token(auth)
        new_refresh = create_refresh_token(auth)

        return TokenResponse(
            access_token=access,
            refresh_token=new_refresh,
        )

    def build_google_authorization_url(
        self,
        redirect_to: str | None = None,
    ) -> str:
        client_id, _, redirect_uri = self._require_google_settings()
        callback_target = self._resolve_frontend_redirect(redirect_to)
        state = self._encode_google_state(callback_target)

        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "prompt": "select_account",
            "access_type": "offline",
            "state": state,
        }
        return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"

    def decode_google_state(self, state: str | None) -> str:
        if not state:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing OAuth state",
            )

        try:
            payload = jwt.decode(
                state,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError as exc:  # pragma: no cover - defensive
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OAuth state",
            ) from exc

        if payload.get("type") != GOOGLE_STATE_TYPE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unexpected OAuth state",
            )

        redirect_to = payload.get("redirect_to")
        if not isinstance(redirect_to, str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid redirect target",
            )

        return redirect_to

    def build_google_success_redirect(
        self,
        redirect_to: str,
        tokens: TokenResponse,
    ) -> str:
        return self._with_fragment(
            redirect_to,
            {
                "access_token": tokens.access_token,
                "refresh_token": tokens.refresh_token,
                "token_type": tokens.token_type,
                "provider": "google",
            },
        )

    def build_google_error_redirect(
        self,
        redirect_to: str,
        error: str,
        description: str | None = None,
    ) -> str:
        params: dict[str, str] = {"error": error}
        if description:
            params["error_description"] = description
        return self._with_fragment(redirect_to, params)

    async def login_with_google_code(self, code: str) -> TokenResponse:
        token_payload = await self._exchange_google_code(code)
        access_token = token_payload.get("access_token")
        if not isinstance(access_token, str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing Google access token",
            )

        userinfo = await self._fetch_google_userinfo(access_token)
        google_id = userinfo.get("sub")
        email = userinfo.get("email")
        email_verified = userinfo.get("email_verified")

        if not isinstance(google_id, str) or not isinstance(email, str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to read Google profile",
            )

        if email_verified is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Google email must be verified",
            )

        user = self._get_or_create_google_user(email=email, google_id=google_id)
        return self._issue_tokens(user)

    def _issue_tokens(self, user: User) -> TokenResponse:
        auth = self._as_auth_user(user)
        access = create_access_token(auth)
        refresh = create_refresh_token(auth)
        return TokenResponse(
            access_token=access,
            refresh_token=refresh,
        )

    def _as_auth_user(self, user: User) -> AuthUser:
        # TODO: load tenant_id, roles, permissions from user/joins
        return AuthUser(
            id=user.id,
            tenant_id=None,
            roles=(),
            permissions=(),
        )

    def _require_google_settings(self) -> tuple[str, str, str]:
        client_id = settings.google_client_id
        client_secret = settings.google_client_secret
        redirect_uri = settings.google_redirect_uri

        if not client_id or not client_secret or not redirect_uri:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Google OAuth is not configured",
            )

        return client_id, client_secret, redirect_uri

    def _resolve_frontend_redirect(self, redirect_to: str | None) -> str:
        base = settings.frontend_app_url.rstrip("/")
        target = redirect_to or DEFAULT_GOOGLE_FRONTEND_REDIRECT

        parsed = urlparse(target)
        if parsed.scheme and parsed.netloc:
            if not target.startswith(base):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Redirect target must point to the frontend origin",
                )
            return target

        if not target.startswith("/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Redirect target must be a path",
            )

        return f"{base}{target}"

    def _encode_google_state(self, redirect_to: str) -> str:
        payload = {
            "redirect_to": redirect_to,
            "nonce": secrets.token_urlsafe(16),
            "type": GOOGLE_STATE_TYPE,
            "exp": datetime.utcnow() + timedelta(minutes=10),
        }
        return jwt.encode(
            payload,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm,
        )

    def _with_fragment(self, url: str, params: dict[str, str]) -> str:
        parsed = urlparse(url)
        existing = dict(parse_qsl(parsed.fragment))
        existing.update(params)
        fragment = urlencode(existing)
        rebuilt = parsed._replace(fragment=fragment)
        return urlunparse(rebuilt)

    async def _exchange_google_code(self, code: str) -> dict[str, Any]:
        client_id, client_secret, redirect_uri = self._require_google_settings()
        data = {
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    GOOGLE_TOKEN_URL,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to exchange Google authorization code",
            ) from exc
        except httpx.HTTPError as exc:  # pragma: no cover - network failure
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Unable to reach Google token endpoint",
            ) from exc

        token_payload = response.json()
        if not isinstance(token_payload, dict):
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Unexpected response from Google token endpoint",
            )

        return token_payload

    async def _fetch_google_userinfo(self, access_token: str) -> dict[str, Any]:
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(GOOGLE_USERINFO_URL, headers=headers)
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to fetch Google profile",
            ) from exc
        except httpx.HTTPError as exc:  # pragma: no cover - network failure
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Unable to reach Google userinfo endpoint",
            ) from exc

        payload = response.json()
        if not isinstance(payload, dict):
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Unexpected Google profile payload",
            )
        return payload

    def _get_or_create_google_user(self, email: str, google_id: str) -> User:
        user = self._user_repo.get_by_google_id(google_id)
        if user:
            return user

        existing_email_user = self._user_repo.get_by_email(email)
        if existing_email_user:
            return self._user_repo.link_google_account(existing_email_user, google_id)

        return self._user_repo.create(email=email, google_id=google_id)
