from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

# Base schema containing common fields for notifications
class NotificationBase(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)

    model_config = ConfigDict(from_attributes=True)

# Schema used for creating a notification
class NotificationCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)

# Schema used for updating a notification
class NotificationUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)
    read: Optional[bool] = None

# Schema representing a single notification response
class NotificationResponse(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    read: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

# Alias for a read notification (used by routes)
class NotificationRead(NotificationResponse):
    pass

# Schema for a list of notifications response
class NotificationListResponse(BaseModel):
    notifications: Optional[List[NotificationRead]] = None
    total: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
