import pytest
from pydantic import ValidationError

from app.schemas.auth import LoginRequest
from app.schemas.user import UserCreate


def test_valid_login_request():
    
    data = LoginRequest(
        email="test@example.com",
        password="12345678",
    )
    
    assert data.email == "test@example.com"
    assert data.password == "12345678"
    
def test_invalid_email():
    
    with pytest.raises(ValidationError):
        LoginRequest(
            email="not_an_email",
            password="12345678"
        )
        
def test_short_password():
    
    with pytest.raises(ValidationError):
        LoginRequest(
            email="test@example.com",
            password="12345678",
        )
        
def test_valid_user_creation():
    
    data = UserCreate(
        email="test@example.com",
        password="12345678",
    )
    
    with pytest.raises(ValidationError):
        data

    # assert data.email == "test@example.com"