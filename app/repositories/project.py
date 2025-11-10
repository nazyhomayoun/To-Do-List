from typing import List
from sqlalchemy.orm import Session
from app.models.project import Project
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    """Repository for Project operations"""
    
    def __init__(self, session: Session):
        super().__init__(Project, session)
    
    def get_by_owner(self, owner_id: int) -> List[Project]:
        """Get all projects by owner"""
        return self.session.query(Project).filter(
            Project.owner_id == owner_id
        ).all()
    
    def search_by_title(self, title: str, owner_id: int = None) -> List[Project]:
        """Search projects by title"""
        query = self.session.query(Project).filter(
            Project.title.ilike(f'%{title}%')
        )
        if owner_id is not None:
            query = query.filter(Project.owner_id == owner_id)
        return query.all()
