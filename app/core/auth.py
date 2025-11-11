# app/core/auth.py
from datetime import datetime, timedelta
from typing import Tuple
import jwt
from passlib.context import CryptContext
from app.config import settings

pwd_ctx = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_ctx.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_ctx.verify(password, hashed)


def create_access_token(subject: str, tenant_id: str, expires_delta: timedelta):
    now = datetime.utcnow()
    data = {
        "sub": subject,
        "tenant_id": tenant_id,
        "iat": now,
        "exp": now + expires_delta,
        "scope": "access",
    }
    return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(subject: str, tenant_id: str, expires_days: int):
    now = datetime.utcnow()
    data = {
        "sub": subject,
        "tenant_id": tenant_id,
        "iat": now,
        "exp": now + timedelta(days=expires_days),
        "scope": "refresh",
    }
    return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_jwt(token: str):
    return jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM],
        options={"verify_aud": False},
    )
