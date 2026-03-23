from datetime import datetime
from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    content: str = Field(..., min_length=1)
    tags: str | None = None
    is_important: bool = False


class NoteResponse(BaseModel):
    id: int
    content: str
    tags: str | None
    is_important: bool
    created_at: datetime

    model_config = {"from_attributes": True}