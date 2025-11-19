from pydantic import BaseModel


class LoginRequest(BaseModel):
    # you can rename to "username" if you prefer
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class OAuthProviderUrlResponse(BaseModel):
    authorization_url: str


class UserRead(BaseModel):
    id: int
    email: str | None = None  # TODO: align with ORM (tenant, roles, etc.)

    class Config:
        from_attributes = True


class RegisterRequest(BaseModel):
    email: str
    password: str
