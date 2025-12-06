from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "TodoList API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A RESTful API for managing tasks, projects and users"
    
    # Database
    DATABASE_URL: str = "sqlite:///./todolist.db"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    class Config:
        case_sensitive = True


settings = Settings()
