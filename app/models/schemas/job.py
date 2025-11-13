from pydantic import BaseModel

class JobRead(BaseModel):
    id: int
    status: str | None = None  # TODO

    class Config:
        from_attributes = True
