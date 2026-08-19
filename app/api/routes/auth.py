from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db), ):
    
    repository = UserRepository(db)
    service = AuthService(repository)
    
    try:
        user = service.create_user(
            email=user_data.email,
            password=user_data.password,
        )
        
        db.commit()
        db.refresh(user)
        
        return user
    
    except ValueError as exc:
        db.rollback()
        
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )