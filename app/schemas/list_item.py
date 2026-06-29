from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ListItemCreate(BaseModel):
    title: str = Field(min_length=1)
    description: Optional[str] = None

class ListItemUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = None
    order: Optional[int] = None
    owner_id: Optional[int] = None

class ListItemResponse(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    owner_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
