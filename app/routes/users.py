from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import UserCreate, UserResponse
from app.database import get_db
from app.models import UserModel

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=201)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    # Consultar si existe un usuario con ese correo
    existing_user = db.query(UserModel).filter(
        UserModel.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code = 409,
            detail = "Email already exists"
        )
    
    # Registrar el usuario
    new_user = UserModel(
        name = user.name,
        email = user.email,
        age = user.age
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{user_id}", response_model=UserResponse, status_code=200)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code = 404,
            detail = "User not found"
        )
    
    return user