from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class TeamCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)


class TeamUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)


class TeamResponse(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
