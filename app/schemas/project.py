from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectBase(BaseModel):
    """Base Project schema"""
    title: str
    description: Optional[str] = None



class ProjectCreate(ProjectBase):
    """Schema for creating a project"""
    owner_id: int


class ProjectResponse(ProjectBase):
    """Schema for project response"""
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
