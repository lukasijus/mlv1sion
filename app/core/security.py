# app/core/security.py
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class AuthUser:
    id: int
    tenant_id: Optional[int]
    roles: Tuple[str, ...]
    permissions: Tuple[str, ...]


def get_current_user() -> AuthUser:
    """TODO: Implement auth dependency (JWT / session)."""
    # e.g. decode JWT, validate, etc.
    raise NotImplementedError
