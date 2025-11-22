from pydantic import BaseModel, Field


class DatasetCreate(BaseModel):
    project_id: int = Field(..., description="Project ID this dataset belongs to")
    name: str = Field(..., description="Dataset name")
    description: str | None = Field(default=None, description="Optional description")


class DatasetRead(BaseModel):
    id: int
    project_id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True
