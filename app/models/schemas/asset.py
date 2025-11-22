from pydantic import BaseModel, Field


class PresignRequest(BaseModel):
    dataset_id: int = Field(..., description="Dataset ID to upload into")
    filename: str = Field(..., description="Object name within the dataset")


class PresignResponse(BaseModel):
    upload_url: str = Field(..., description="Presigned URL for uploading the asset")
    object_key: str = Field(..., description="Storage object key within the bucket")
    bucket: str = Field(..., description="Target bucket for the upload")
