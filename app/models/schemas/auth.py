from pydantic import BaseModel

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str

class UserRead(BaseModel):
    id: int
    email: str | None = None  # TODO: align with ORM

    class Config:
        from_attributes = True
