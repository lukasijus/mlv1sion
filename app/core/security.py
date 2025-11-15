# app/core/security.py
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Tuple

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings  # you already have Settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@dataclass(frozen=True)
class AuthUser:
    id: int
    tenant_id: Optional[int]
    roles: Tuple[str, ...]
    permissions: Tuple[str, ...]


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def _encode_token(
    auth: AuthUser,
    expires_delta: timedelta,
    token_type: str,
) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": str(auth.id),
        "tenant_id": auth.tenant_id,
        "roles": list(auth.roles),
        "permissions": list(auth.permissions),
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def create_access_token(auth: AuthUser) -> str:
    return _encode_token(
        auth,
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
        token_type="access",
    )


def create_refresh_token(auth: AuthUser) -> str:
    return _encode_token(
        auth,
        expires_delta=timedelta(days=settings.refresh_token_expire_days),
        token_type="refresh",
    )


def decode_token(token: str, expected_type: str = "access") -> AuthUser:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    if payload.get("type") != expected_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong token type",
        )

    try:
        user_id = int(payload["sub"])
    except (KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    return AuthUser(
        id=user_id,
        tenant_id=payload.get("tenant_id"),
        roles=tuple(payload.get("roles", [])),
        permissions=tuple(payload.get("permissions", [])),
    )


def get_current_user(token: str = Depends(oauth2_scheme)) -> AuthUser:
    """FastAPI dependency: decode Bearer token into AuthUser."""
    return decode_token(token, expected_type="access")
