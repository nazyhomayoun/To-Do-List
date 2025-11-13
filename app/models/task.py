from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin
from datetime import datetime
import enum


class TaskStatus(enum.Enum):
    """Task status enumeration"""
    TODO = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'
    CANCELLED = 'CANCELLED'
    OVERDUE = 'OVERDUE'


class TaskPriority(enum.Enum):
    """Task priority enumeration"""
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    URGENT = 'URGENT'


class Task(Base, TimestampMixin):
    """Task model"""
    
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    deadline = Column(DateTime, nullable=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    
    # Relationships
    project = relationship('Project', back_populates='tasks')
    
    @property
    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if self.deadline is None:
            return False
        if self.status in [TaskStatus.DONE, TaskStatus.CANCELLED]:
            return False
        return datetime.utcnow() > self.deadline
    
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status={self.status.value}, priority={self.priority.value})>"