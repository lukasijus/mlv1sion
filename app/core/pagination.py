from pydantic import BaseModel

class PaginationParams(BaseModel):
    """Basic pagination params."""
    limit: int = 50
    offset: int = 0
