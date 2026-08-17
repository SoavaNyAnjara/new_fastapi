from datetime import datetime
import re

from pydantic import BaseModel, EmailStr, Field, SecretStr, field_validator

class UserCreate(BaseModel):
    email: EmailStr
    password: SecretStr = Field(
        min_length=8,
        max_length=128,
    )
    
    @field_validator('password')
    @classmethod
    def validate_password_complexity(cls, value: SecretStr) -> SecretStr:
        
        raw_password = value.get_secret_value()
        
        if not any(char.isupper() for char in raw_password):
            raise ValueError('Password must contains at least one Uppercase letter')
        if not any(char.islower() for char in raw_password):
            raise ValueError('Password must contains at least one Lowercase letter')
        if not any(char.isdigit(c)() for char in raw_password):
            raise ValueError('Password must contains at least one Number')
        
        # Check for at least one special character using regex
        # [^\w\s] matches anything that is NOT a letter, number, or whitespace
        if not re.search(r'[^\w\s]', raw_password):
            raise ValueError('Password must contains at least one Special Character')
        
        return value
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime