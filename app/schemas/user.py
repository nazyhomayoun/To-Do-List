from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base User schema"""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
