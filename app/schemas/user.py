from datetime import datetime
import re

from pydantic import BaseModel, EmailStr, Field, SecretStr, field_validator, ConfigDict

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
        
        errors = []
        if not any(char.isupper() for char in raw_password): errors.append("uppercase")
        if not any(char.islower() for char in raw_password): errors.append("lowercase")
        if not any(char.isdigit() for char in raw_password): errors.append("number")
        if not re.search(r'[^\w\s]', raw_password): errors.append("special")

        if errors:
            # Si errors = ["uppercase", "number"], cela donnera : "one uppercase, one number"
            detail = ", ".join(f"one {err}" for err in errors)
            raise ValueError(f"Password must contains at least {detail}")

        
        return value
    
class UserResponse(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime