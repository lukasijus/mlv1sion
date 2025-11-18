from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse

from app.api.deps import get_auth_service
from app.services.auth_service import AuthService

router = APIRouter(tags=["auth"])


@router.get("/auth/google/callback", include_in_schema=False)
async def google_callback(
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    error_description: str | None = None,
    svc: AuthService = Depends(get_auth_service),
):
    redirect_target = svc.decode_google_state(state)

    if error:
        failure_url = svc.build_google_error_redirect(
            redirect_target,
            error=error,
            description=error_description,
        )
        return RedirectResponse(failure_url, status_code=status.HTTP_302_FOUND)

    if not code:
        failure_url = svc.build_google_error_redirect(
            redirect_target,
            error="missing_code",
            description="Google did not return an authorization code",
        )
        return RedirectResponse(failure_url, status_code=status.HTTP_302_FOUND)

    tokens = await svc.login_with_google_code(code)
    success_url = svc.build_google_success_redirect(redirect_target, tokens)
    return RedirectResponse(success_url, status_code=status.HTTP_302_FOUND)
