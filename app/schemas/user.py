from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base User schema"""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
