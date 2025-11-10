from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User operations"""
    
    def __init__(self, session: Session):
        super().__init__(User, session)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.session.query(User).filter(
            User.username == username
        ).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.session.query(User).filter(
            User.email == email
        ).first()
    
    def username_exists(self, username: str) -> bool:
        """Check if username exists"""
        return self.session.query(User).filter(
            User.username == username
        ).count() > 0
    
    def email_exists(self, email: str) -> bool:
        """Check if email exists"""
        return self.session.query(User).filter(
            User.email == email
        ).count() > 0
