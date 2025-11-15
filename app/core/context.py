# app/core/context.py
from dataclasses import dataclass
from typing import Optional, Tuple

from fastapi import Depends

from app.core.security import get_current_user, AuthUser


@dataclass(frozen=True)
class UserContext:
    user_id: int
    tenant_id: Optional[int]
    roles: Tuple[str, ...]
    permissions: Tuple[str, ...]


def get_user_context(current: AuthUser = Depends(get_current_user)) -> UserContext:
    return UserContext(
        user_id=current.id,
        tenant_id=current.tenant_id,
        roles=current.roles,
        permissions=current.permissions,
    )
