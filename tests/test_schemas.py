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
        password="M*a2345678",
    )

    assert data.email == "test@example.com"
    
def test_invalid_password_raises_validation_error():
    
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            email="test@test.com",
            password="simplepassword", 
        )
    
    # 2. On extrait le message d'erreur brut de Pydantic v2
    error_msg = exc_info.value.errors()[0]['msg']
    
    # On l'affiche dans le terminal (visible avec la commande pytest -s)
    print(f"\nMessage généré par votre code : {error_msg}")
    
    # 3. L'assertion adaptée à votre nouvelle logique
    # On vérifie que le début du message est correct
    assert "Password must contains at least" in error_msg