# app/db/session.py

import os
from contextlib import contextmanager
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.models.base import Base

# Load environment variables
load_dotenv()

# Database configuration
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'todolist_db')

# Construct database URL
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True,  # Enable connection health checks
    pool_size=5,
    max_overflow=10
)
try:
    with engine.connect() as conn:
        print("✅ Connection successful")
except Exception as e:
    print("❌ Connection failed:", e)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class DatabaseSession:
    """Context manager for database sessions"""

    def __init__(self):
        self.session: Session = SessionLocal()

    def __enter__(self) -> Session:
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session.rollback()
        self.session.close()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Dependency function for getting database session

    Usage:
        with get_db_session() as db:
            # Your database operations
            pass
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    """
    Initialize database by creating all tables
    Note: In production, use Alembic migrations instead
    """
    Base.metadata.create_all(bind=engine)


def drop_db():
    """
    Drop all tables from database

    Warning: This will delete all data!
    """
    Base.metadata.drop_all(bind=engine)


# For testing purposes
def get_test_db_session():
    """Get a test database session (for unit tests)"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()