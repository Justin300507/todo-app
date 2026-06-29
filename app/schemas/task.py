import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class TaskBase(BaseModel):
    title: str = Field(min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)
    status: str = Field(min_length=1)
    assignee_id: Optional[int] = None
    due_date: Optional[datetime.datetime] = None
    order: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)
    status: Optional[str] = Field(default=None, min_length=1)
    assignee_id: Optional[int] = None
    due_date: Optional[datetime.datetime] = None
    order: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class TaskRead(TaskBase):
    id: int
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    model_config = ConfigDict(from_attributes=True)

# Backward compatibility alias
TaskResponse = TaskRead