from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas import project as schemas
from app.api.deps import get_db
from app.api import deps
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project import ProjectService

router = APIRouter()


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project"""
    project_service = ProjectService(db)
    try:
        created_project = project_service.create_project(
            title=project.title,
            description=project.description,
            owner_id=project.owner_id
        )
        return created_project
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[schemas.ProjectResponse])
def read_projects(
    owner_id: Optional[int] = Query(None),
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    db: Session = Depends(deps.get_db)
):
    print(f"🔍 GET /projects called with owner_id={owner_id}, skip={skip}, limit={limit}")
    try:
        projects = ProjectService.get_projects(db=db, owner_id=owner_id, skip=skip, limit=limit)
        print(f"✅ Found {len(projects)} projects")
        return projects
    except Exception as e:
        print(f"❌ Error in get_projects: {str(e)}")
        print(f"❌ Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        raise


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get a project by ID"""
    project_service = ProjectService(db)
    project = project_service.get_project_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    return project
