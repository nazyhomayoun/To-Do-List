from typing import Optional
import hashlib
from sqlalchemy.orm import Session
from app.models.user import User
from typing import List, Optional
from app.repositories.user import UserRepository
from app.exceptions import ValidationException, DuplicateException


class UserService:
    """Service for User business logic"""
    
    def __init__(self, session: Session):
        self.repository = UserRepository(session)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, email: str, password: str) -> User:
        """Create a new user"""
        # Validation
        if len(username) < 3:
            raise ValidationException(
                "Username must be at least 3 characters",
                {'username': username}
            )
        
        if '@' not in email:
            raise ValidationException(
                "Invalid email format",
                {'email': email}
            )
        
        if len(password) < 6:
            raise ValidationException(
                "Password must be at least 6 characters"
            )
        
        # Check duplicates
        if self.repository.username_exists(username):
            raise DuplicateException(
                "Username already exists",
                {'username': username}
            )
        
        if self.repository.email_exists(email):
            raise DuplicateException(
                "Email already exists",
                {'email': email}
            )
        
        # Create user
        user = User(
            username=username,
            email=email,
            password_hash=self.hash_password(password)
        )
        
        return self.repository.create(user)
    
    def get_user_by_id(self, user_id: int) -> User:
        """Get user by ID"""
        return self.repository.get_by_id_or_fail(user_id)

    @staticmethod
    def get_users(
            db: Session,
            skip: int = 0,
            limit: int = 100
    ) -> List[User]:
        """Get all users with pagination"""
        return db.query(User).offset(skip).limit(limit).all()
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate user"""
        user = self.repository.get_by_username(username)
        if user is None:
            return None
        
        password_hash = self.hash_password(password)
        if user.password_hash == password_hash:
            return user
        
        return None
