from pydantic import BaseModel

class ProjectRead(BaseModel):
    id: int
    name: str | None = None  # TODO: align with ORM

    class Config:
        from_attributes = True
