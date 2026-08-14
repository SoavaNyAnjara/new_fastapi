from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.config import settings
from app.core.security import hash_password
import pytest
from sqlalchemy.exc import IntegrityError


engine = create_engine(settings.DATABASE_URL)

def test_get_by_email():
    with Session(engine) as db:
        
        user = User(email="test@test.com", password_hash="fake_hash")
        
        db.add(user)
        db.commit()
        
        repository = UserRepository(db)
        
        result = repository.get_by_email("test@test.com")
        
        assert result is not None
        assert result.email == "test@test.com"
        
        db.delete(user)
        db.commit()
        
def test_create_user():
    with Session(engine) as db:
        
        repository = UserRepository(db)
        
        password = "12345!"
        password_hash = hash_password(password)
        
        user = repository.create(email="test@test.com", password_hash=password_hash)
        
        db.commit()
        
        assert user.id is not None
        assert user.email == "test@test.com"
        assert user.password_hash != password
        assert user.password_hash == password_hash
        
        db.delete(user)
        db.commit()
        
def test_duplicate_email_is_rejected():
    with Session(engine) as db:
        
        repository = UserRepository(db)
        
        password_hash = hash_password('12345!')
        
        repository.create(
            email='duplicate@test.com',
            password_hash=password_hash,        
        )
        
        db.commit()        
        
        with pytest.raises(IntegrityError):
            repository.create(
                email='duplicate@test.com',
                password_hash=password_hash,        
            )
            db.commit()
            
        db.rollback()
        
        user = repository.get_by_email("duplicate@test.com")
        
        assert user is not None
        
        db.delete(user)
        db.commit()