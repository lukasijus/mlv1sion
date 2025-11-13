from pydantic import BaseModel

class DatasetRead(BaseModel):
    id: int
    name: str | None = None  # TODO

    class Config:
        from_attributes = True
