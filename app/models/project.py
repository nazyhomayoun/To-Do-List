from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Project(Base, TimestampMixin):
    """Project model"""

    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    owner = relationship('User', back_populates='projects')
    tasks = relationship('Task', back_populates='project', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Project(id={self.id}, title='{self.title}', owner_id={self.owner_id})>"