from pydantic import BaseModel, Field, EmailStr, model_validator, field_validator
import re

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50) # Los ... son para indicar que el campo es obligatorio
    email: EmailStr
    age: int = Field(..., ge=18, le=65)
    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("The password must contain at least one uppercase letter")
        
        if not re.search(r"[a-z]", v):
            raise ValueError("The password must contain at least one lowercase letter")
        
        if not re.search(r"[0-9]", v):
            raise ValueError("The password must contain at least one number")
        
        if not re.search(r"[!@#$_]", v):
            raise ValueError("The password must contain at least one special character")
        
        return v

class UserUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50) # Los ... son para indicar que el campo es obligatorio
    email: EmailStr
    age: int = Field(..., ge=18, le=65)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int

    # Permite convertir modelos SQLAlchemy a respuestas FastAPI
    model_config = {
        "from_attributes": True
    }

class UserPatch(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=50)
    email: EmailStr | None = None
    age: int | None = Field(None, ge=18, le=65)

    """
    Validaciones dentro del esquema
    - No se acepta json vacío {}
    - No se acepta json con valor null en alguno de los campos
    """
    @model_validator(mode="after")
    def validate_patch(self):
        if not self.model_fields_set:
            raise ValueError("At least one field is required")
        
        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"Field {field} cannot be null")
        
        return self

class UserLogin(BaseModel):
    email: EmailStr
    password: str