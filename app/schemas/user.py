from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

from app.utils.password_validator import validate_password_strength


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)  # Los ... son para indicar que el campo es obligatorio
    email: EmailStr
    age: int = Field(..., ge=18, le=65)
    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password_strength(v)


class UserUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)  # Los ... son para indicar que el campo es obligatorio
    email: EmailStr
    age: int = Field(..., ge=18, le=65)


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int

    # Permite convertir modelos SQLAlchemy a respuestas FastAPI
    model_config = {"from_attributes": True}


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


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    message: str
    token: str | None = None


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        return validate_password_strength(v)


class ResetPasswordResponse(BaseModel):
    message: str
