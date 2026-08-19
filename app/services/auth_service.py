from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        
    def create_user(
        self,
        email: str,
        password: str,
    ) -> User:
        
        existing_user = self.user_repository.get_by_email(email)
        
        if existing_user:
            raise ValueError(
                "An existing user with this email is already exists"
            )
            
        password_hash = hash_password(password.get_secret_value())
        
        return self.user_repository.create(
            email=email,
            password_hash=password_hash,
            )
        
    def authenticate(
        self,
        email: str,
        password: str,
    ) -> User | None:
        user = self.user_repository.get_by_email(email)
        
        if user is None:
            return None
        
        if not user.is_active:
            return None
        
        if not verify_password(
            password,
            user.password_hash,
        ):
            return None
        
        return user
    
    def create_tokens(
        self,
        user: User,
    ) -> dict[str, str]:
        
        return {
            "access_token": create_access_token(user.id),
            "refresh_token": create_refresh_token(user.id),
        }