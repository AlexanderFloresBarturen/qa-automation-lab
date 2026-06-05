from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50) # Los ... son para indicar que el campo es obligatorio
    email: EmailStr
    age: int = Field(..., ge=18, le=65)