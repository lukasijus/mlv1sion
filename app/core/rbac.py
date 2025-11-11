# app/core/rbac.py
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.auth import decode_jwt
from typing import Optional, List

security = HTTPBearer(auto_error=False)


def get_current_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
):
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = credentials.credentials
    payload = decode_jwt(token)
    return payload


def require_roles(allowed: List[str]):
    def dependency(payload=Depends(get_current_token)):
        roles = payload.get("roles", [])
        tenant_id = payload.get("tenant_id")
        if not tenant_id:
            raise HTTPException(status_code=403, detail="Tenant required")
        if not set(allowed).intersection(set(roles)):
            raise HTTPException(status_code=403, detail="Insufficient role")
        return payload

    return dependency
