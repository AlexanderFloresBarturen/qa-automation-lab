from pydantic import BaseModel, EmailStr

class UserDetailResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int

    # Permite convertir modelos SQLAlchemy a respuestas FastAPI
    model_config = {"from_attributes": True}
