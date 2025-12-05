# app/models/task.py
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class TaskStatus(enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    CANCELLED = "CANCELLED"
    OVERDUE = "OVERDUE"


class TaskPriority(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Task(Base, TimestampMixin):
    """Task model"""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    deadline = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)

    # Foreign Keys (فقط یکبار!)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="assigned_tasks")

    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if self.deadline and self.status not in [TaskStatus.DONE, TaskStatus.CANCELLED]:
            return datetime.now() > self.deadline
        return False

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status={self.status.value})>"
