from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class AuthCreate(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)
    display_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class AuthUpdate(BaseModel):
    email: Optional[str] = Field(default=None, min_length=1)
    password: Optional[str] = Field(default=None, min_length=1)
    display_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class AuthResponse(BaseModel):
    id: int
    email: Optional[str] = None
    display_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)

    model_config = ConfigDict(from_attributes=True)

class RegisterRequest(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)
    display_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# Alias for registration request expected by routes
class SignupRequest(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)
    display_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str
    display_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
