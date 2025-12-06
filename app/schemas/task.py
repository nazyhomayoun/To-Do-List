from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.task import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    """Base Task schema"""
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.TODO


class TaskCreate(TaskBase):
    """Schema for creating a task"""
    project_id: int
    assignee_id: Optional[int] = None
    deadline: Optional[datetime] = None


class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    deadline: Optional[datetime] = None


class TaskResponse(TaskBase):
    """Schema for task response"""
    id: int
    project_id: int
    assignee_id: Optional[int] = None
    deadline: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
