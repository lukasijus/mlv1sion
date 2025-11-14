from pydantic import BaseModel


class DatasetRead(BaseModel):
    id: int
    project_id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True
