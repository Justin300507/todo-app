from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class StatsCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)


class StatsUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)


class StatsResponse(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    total_members: Optional[int] = None
    active_today: Optional[int] = None
    revenue_this_month: Optional[float] = None
    classes_today: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
