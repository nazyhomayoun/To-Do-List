from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.task import Task, TaskStatus, TaskPriority
from app.repositories.base import BaseRepository


class TaskRepository(BaseRepository[Task]):
    """Repository for Task operations"""
    
    def __init__(self, session: Session):
        super().__init__(Task, session)
    
    def get_by_project(self, project_id: int) -> List[Task]:
        """Get all tasks by project"""
        return self.session.query(Task).filter(
            Task.project_id == project_id
        ).all()
    
    def get_by_status(self, status: TaskStatus, project_id: int = None) -> List[Task]:
        """Get tasks by status"""
        query = self.session.query(Task).filter(Task.status == status)
        if project_id is not None:
            query = query.filter(Task.project_id == project_id)
        return query.all()
    
    def get_by_priority(self, priority: TaskPriority, project_id: int = None) -> List[Task]:
        """Get tasks by priority"""
        query = self.session.query(Task).filter(Task.priority == priority)
        if project_id is not None:
            query = query.filter(Task.project_id == project_id)
        return query.all()
    
    def get_overdue_tasks(self) -> List[Task]:
        """Get all overdue tasks (not done/cancelled and deadline passed)"""
        now = datetime.utcnow()
        return self.session.query(Task).filter(
            and_(
                Task.deadline < now,
                Task.status.notin_([TaskStatus.DONE, TaskStatus.CANCELLED, TaskStatus.OVERDUE])
            )
        ).all()
    
    def search_by_title(self, title: str, project_id: int = None) -> List[Task]:
        """Search tasks by title"""
        query = self.session.query(Task).filter(
            Task.title.ilike(f'%{title}%')
        )
        if project_id is not None:
            query = query.filter(Task.project_id == project_id)
        return query.all()
