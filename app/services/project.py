from typing import List
from sqlalchemy.orm import Session
from app.models.project import Project
from app.repositories.project import ProjectRepository
from app.exceptions import ValidationException, NotFoundException


class ProjectService:
    """Service for Project business logic"""
    
    def __init__(self, session: Session):
        self.repository = ProjectRepository(session)
    
    def create_project(self, title: str, owner_id: int, description: str = None) -> Project:
        """Create a new project"""
        if len(title.strip()) == 0:
            raise ValidationException(
                "Project title cannot be empty"
            )
        
        project = Project(
            title=title.strip(),
            description=description,
            owner_id=owner_id
        )
        
        return self.repository.create(project)
    
    def get_project_by_id(self, project_id: int) -> Project:
        """Get project by ID"""
        return self.repository.get_by_id_or_fail(project_id)
    
    def get_user_projects(self, owner_id: int) -> List[Project]:
        """Get all projects for a user"""
        return self.repository.get_by_owner(owner_id)
    
    def update_project(self, project_id: int, title: str = None, description: str = None) -> Project:
        """Update project"""
        project = self.repository.get_by_id_or_fail(project_id)
        
        if title is not None:
            if len(title.strip()) == 0:
                raise ValidationException("Project title cannot be empty")
            project.title = title.strip()
        
        if description is not None:
            project.description = description
        
        return self.repository.update(project)
    
    def delete_project(self, project_id: int) -> None:
        """Delete project"""
        self.repository.delete_by_id(project_id)
    
    def search_projects(self, title: str, owner_id: int = None) -> List[Project]:
        """Search projects by title"""
        return self.repository.search_by_title(title, owner_id)
