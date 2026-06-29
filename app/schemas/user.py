from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

class UserCreate(BaseModel):
    """Schema for creating a new user (admin or registration)."""

    email: str = Field(..., min_length=1, description="User e‑mail address")
    username: str = Field(..., min_length=1, description="Unique username")
    password: str = Field(..., min_length=1, description="Plain‑text password")
    display_name: Optional[str] = Field(None, min_length=1, description="Public name shown in UI")
    role: Optional[str] = Field(None, min_length=1, description="User role, e.g. 'admin' or 'user'")

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    """Schema for partial updates of an existing user."""

    email: Optional[str] = Field(None, min_length=1)
    username: Optional[str] = Field(None, min_length=1)
    password: Optional[str] = Field(None, min_length=1)
    display_name: Optional[str] = Field(None, min_length=1)
    role: Optional[str] = Field(None, min_length=1)

    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    """Schema returned by the API for a user record."""

    id: int
    email: Optional[str] = None
    username: Optional[str] = None
    display_name: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class UserRead(BaseModel):
    """Schema for reading user data (alias of UserResponse)."""

    id: int
    email: Optional[str] = None
    username: Optional[str] = None
    display_name: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# ---------------------------------------------------------------------------
# Authentication related schemas - they live in this file per project contract
# ---------------------------------------------------------------------------
