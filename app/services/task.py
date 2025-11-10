from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.task import Task, TaskStatus, TaskPriority
from app.repositories.task import TaskRepository
from app.exceptions import ValidationException


class TaskService:
    """Service for Task business logic"""
    
    def __init__(self, session: Session):
        self.repository = TaskRepository(session)
    
    def create_task(
        self,
        title: str,
        project_id: int,
        description: str = None,
        priority: TaskPriority = TaskPriority.MEDIUM,
        deadline: datetime = None
    ) -> Task:
        """Create a new task"""
        if len(title.strip()) == 0:
            raise ValidationException("Task title cannot be empty")
        
        if deadline is not None and deadline < datetime.utcnow():
            raise ValidationException("Deadline cannot be in the past")
        
        task = Task(
            title=title.strip(),
            description=description,
            project_id=project_id,
            priority=priority,
            deadline=deadline,
            status=TaskStatus.TODO
        )
        
        return self.repository.create(task)
    
    def get_task_by_id(self, task_id: int) -> Task:
        """Get task by ID"""
        return self.repository.get_by_id_or_fail(task_id)
    
    def get_project_tasks(self, project_id: int) -> List[Task]:
        """Get all tasks for a project"""
        return self.repository.get_by_project(project_id)
    
    def update_task(
        self,
        task_id: int,
        title: str = None,
        description: str = None,
        priority: TaskPriority = None,
        deadline: datetime = None
    ) -> Task:
        """Update task"""
        task = self.repository.get_by_id_or_fail(task_id)
        
        if title is not None:
            if len(title.strip()) == 0:
                raise ValidationException("Task title cannot be empty")
            task.title = title.strip()
        
        if description is not None:
            task.description = description
        
        if priority is not None:
            task.priority = priority
        
        if deadline is not None:
            if deadline < datetime.utcnow():
                raise ValidationException("Deadline cannot be in the past")
            task.deadline = deadline
        
        return self.repository.update(task)
    
    def change_task_status(self, task_id: int, status: TaskStatus) -> Task:
        """Change task status"""
        task = self.repository.get_by_id_or_fail(task_id)
        task.status = status
        return self.repository.update(task)
    
    def delete_task(self, task_id: int) -> None:
        """Delete task"""
        self.repository.delete_by_id(task_id)
    
    def get_tasks_by_status(self, status: TaskStatus, project_id: int = None) -> List[Task]:
        """Get tasks by status"""
        return self.repository.get_by_status(status, project_id)
    
    def get_tasks_by_priority(self, priority: TaskPriority, project_id: int = None) -> List[Task]:
        """Get tasks by priority"""
        return self.repository.get_by_priority(priority, project_id)
    
    def close_overdue_tasks(self) -> int:
        """Close all overdue tasks - returns count of closed tasks"""
        overdue_tasks = self.repository.get_overdue_tasks()
        count = 0
        
        for task in overdue_tasks:
            task.status = TaskStatus.OVERDUE
            self.repository.update(task)
            count += 1
        
        return count
