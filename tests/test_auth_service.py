from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import decode_token
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


engine = create_engine(settings.DATABASE_URL)

def test_create_user_and_authenticate():
    
    with Session(engine) as db:
        
        repository = UserRepository(db)
        service = AuthService(repository)
        
        user = service.create_user(
            email="test@test.com",
            password="12345!"
        )
        
        assert user.id is not None
        assert user.email == "test@test.com"
        assert user.password_hash != "12345!"
        
        authenticated_user = service.authenticate(
            email="test@test.com",
            password="12345!",
        )
        
        assert authenticated_user is not None
        assert authenticated_user.id == user.id
        
        db.delete(user)
        db.commit()
        
def test_wrong_password_is_rejected():
    
    with Session(engine) as db:
        
        repository = UserRepository(db)
        service = AuthService(repository)
        
        user = service.create_user(
            email="wrong_password@test.com",
            password="realpass!",
        )
        
        db.commit()
        
        authenticated_user = service.authenticate(
            email="wrong_password@test.com",
            password="wrongpass!",
        )
        
        assert authenticated_user is None
        
        db.delete(user)
        db.commit()
        
def test_create_tokens():
    
    with Session(engine) as db:
        
        repository = UserRepository(db)
        service = AuthService(repository)
        
        user = service.create_user(
            email="token@test.com",
            password="12345!",
        )
        
        db.commit()
        
        tokens = service.create_tokens(user)
        
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        
        access_payload = decode_token(
            tokens["access_token"]
        )
        
        refresh_payload = decode_token(
            tokens["refresh_token"]
        )
        
        assert access_payload["type"] == "access"
        assert access_payload["sub"] == str(user.id)
        
        assert refresh_payload["type"] == "refresh"
        assert refresh_payload["sub"] == str(user.id)
        
        db.delete(user)
        db.commit()