from pydantic import BaseModel, EmailStr, Field, field_validator

from app.utils.password_validator import validate_password_strength

class CreateUserRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)  # Los ... son para indicar que el campo es obligatorio
    email: EmailStr
    age: int = Field(..., ge=18, le=65)
    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password_strength(v)

class UserDetailResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int

    # Permite convertir modelos SQLAlchemy a respuestas FastAPI
    model_config = {"from_attributes": True}

class UpdateUserRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)  # Los ... son para indicar que el campo es obligatorio
    email: EmailStr
    age: int = Field(..., ge=18, le=65)