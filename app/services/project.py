from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.project import Project
from app.repositories.project import ProjectRepository
from app.exceptions import ValidationException


class ProjectService:
    """Service layer for Project business logic"""

    def __init__(self, session: Session):
        self.repository = ProjectRepository(session)

    def create_project(self, title: str, owner_id: int, description: Optional[str] = None) -> Project:
        """Create a new project and link it to an owner (user)"""
        if not title or len(title.strip()) == 0:
            raise ValidationException("Project title cannot be empty")

        if len(title) > 100:
            raise ValidationException("Project title is too long (max 100 characters)")

        if owner_id is None:
            raise ValidationException("Project must have an owner_id")

        project = Project(
            title=title.strip(),
            description=description,
            owner_id=owner_id
        )

        return self.repository.create(project)

    def get_project_by_id(self, project_id: int) -> Project:
        """Retrieve a project by its ID"""
        return self.repository.get_by_id_or_fail(project_id)

    def get_all_projects(self) -> List[Project]:
        """Retrieve all projects"""
        return self.repository.get_all()

    def update_project(
        self, project_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Project:
        """Update a project's title or description"""
        project = self.repository.get_by_id_or_fail(project_id)

        if title is not None:
            if len(title.strip()) == 0:
                raise ValidationException("Project title cannot be empty")
            if len(title) > 100:
                raise ValidationException("Project title is too long (max 100 characters)")
            project.title = title.strip()

        if description is not None:
            project.description = description

        return self.repository.update(project)

    @staticmethod
    def get_projects(
            db: Session,
            owner_id: Optional[int] = None,
            skip: int = 0,
            limit: int = 100
    ) -> List[Project]:
        """Get all projects with optional filtering and pagination"""
        query = db.query(Project)

        if owner_id:
            query = query.filter(Project.owner_id == owner_id)

        return query.offset(skip).limit(limit).all()

    def delete_project(self, project_id: int) -> None:
        """Delete a project by its ID"""
        self.repository.delete_by_id(project_id)

    def search_projects(self, title: str) -> List[Project]:
        """Search projects by part of their title"""
        return self.repository.search_by_title(title)
