from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class SeedCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)

class SeedUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class SeedResponse(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

