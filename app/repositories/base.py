from typing import TypeVar, Generic, List, Optional, Type
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.base import Base
from app.exceptions import (
    NotFoundException,
    DuplicateException,
    DatabaseException
)

T = TypeVar('T', bound=Base)


class BaseRepository(Generic[T]):
    """Base repository with common CRUD operations"""
    
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session
    
    def create(self, entity: T) -> T:
        """Create a new entity"""
        try:
            self.session.add(entity)
            self.session.flush()
            self.session.refresh(entity)
            return entity
        except IntegrityError as e:
            self.session.rollback()
            raise DuplicateException(
                f"Duplicate {self.model.__name__} found",
                {'error': str(e.orig)}
            )
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseException(
                f"Failed to create {self.model.__name__}",
                {'error': str(e)}
            )
    
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Get entity by ID"""
        try:
            return self.session.query(self.model).filter(
                self.model.id == entity_id
            ).first()
        except SQLAlchemyError as e:
            raise DatabaseException(
                f"Failed to get {self.model.__name__} by ID",
                {'id': entity_id, 'error': str(e)}
            )
    
    def get_by_id_or_fail(self, entity_id: int) -> T:
        """Get entity by ID or raise NotFoundException"""
        entity = self.get_by_id(entity_id)
        if entity is None:
            raise NotFoundException(
                f"{self.model.__name__} not found",
                {'id': entity_id}
            )
        return entity
    
    def get_all(self) -> List[T]:
        """Get all entities"""
        try:
            return self.session.query(self.model).all()
        except SQLAlchemyError as e:
            raise DatabaseException(
                f"Failed to get all {self.model.__name__}",
                {'error': str(e)}
            )
    
    def update(self, entity: T) -> T:
        """Update an entity"""
        try:
            self.session.flush()
            self.session.refresh(entity)
            return entity
        except IntegrityError as e:
            self.session.rollback()
            raise DuplicateException(
                f"Duplicate {self.model.__name__} found during update",
                {'error': str(e.orig)}
            )
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseException(
                f"Failed to update {self.model.__name__}",
                {'error': str(e)}
            )
    
    def delete(self, entity: T) -> None:
        """Delete an entity"""
        try:
            self.session.delete(entity)
            self.session.flush()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseException(
                f"Failed to delete {self.model.__name__}",
                {'error': str(e)}
            )
    
    def delete_by_id(self, entity_id: int) -> None:
        """Delete entity by ID"""
        entity = self.get_by_id_or_fail(entity_id)
        self.delete(entity)
