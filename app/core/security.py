from typing import Any

def get_current_user() -> Any:
    """TODO: Implement auth dependency (JWT / session)."""
    raise NotImplementedError

def require_tenant_access() -> None:
    """TODO: Implement tenant/role checks."""
    raise NotImplementedError
