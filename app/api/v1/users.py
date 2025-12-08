from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas import user as schemas
from app.api.deps import get_db
from app.api import deps
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    user_service = UserService(db)
    try:
        created_user = user_service.create_user(
            username=user.username,
            email=user.email,
            password=user.password
        )
        return created_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[schemas.UserResponse])
def read_users(
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    db: Session = Depends(deps.get_db)
):
    print(f"🔍 GET /users called with skip={skip}, limit={limit}")
    try:
        users = UserService.get_users(db=db, skip=skip, limit=limit)
        print(f"✅ Found {len(users)} users")
        return users
    except Exception as e:
        print(f"❌ Error in get_users: {str(e)}")
        print(f"❌ Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        raise

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a user by ID"""
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user
