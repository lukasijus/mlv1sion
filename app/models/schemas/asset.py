from pydantic import BaseModel

class AssetRead(BaseModel):
    id: int
    filename: str | None = None  # TODO

    class Config:
        from_attributes = True
