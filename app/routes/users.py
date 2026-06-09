from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.schemas import UserCreate, UserResponse, UserUpdate
from app.dependencies import get_db
from app.models import UserModel

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=201)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    # Consultar si existe un usuario con ese correo
    existing_user = db.query(UserModel).filter(
        UserModel.email == user.email,
        UserModel.is_active.is_(True)
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
    user_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(
        UserModel.id == user_id,
        UserModel.is_active.is_(True)
    ).first()

    if not user:
        raise HTTPException(
            status_code = 404,
            detail = "User not found"
        )
    
    return user

@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(
        UserModel.id == user_id,
        UserModel.is_active.is_(True)
    ).first()

    if not user:
        raise HTTPException(
            status_code = 404,
            detail = "User not found"
        )
    
    user.is_active = False

    db.commit()

    return

@router.put("/{user_id}", response_model=UserResponse, status_code=200)
def update_user(
    user: UserUpdate,
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    user_to_update = db.query(UserModel).filter(
        UserModel.id == user_id,
        UserModel.is_active.is_(True)
    ).first()

    if not user_to_update:
        raise HTTPException(
            status_code = 404,
            detail = "User not found"
        )
    
    existing_email = db.query(UserModel).filter(
        UserModel.email == user.email,
        UserModel.id != user_id,
        UserModel.is_active.is_(True)
    ).first()

    if existing_email:
        raise HTTPException(
            status_code = 409,
            detail = "Email already exists"
        )
    
    user_to_update.name = user.name
    user_to_update.email = user.email
    user_to_update.age = user.age

    db.commit()
    db.refresh(user_to_update)

    return user_to_update