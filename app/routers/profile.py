from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.user_model import UserModel
from app.schemas.profile import ProfilePatch, ProfileResponse, ProfileUpdate
from app.security.dependencies import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/", response_model=ProfileResponse, status_code=200)
def get_user_profile(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user


@router.delete("/", status_code=204)
def delete_user_profile(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.is_active = False

    db.commit()

    return


@router.put("/", response_model=ProfileResponse, status_code=200)
def update_user_profile(user: ProfileUpdate, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    existing_email = db.query(UserModel).filter(UserModel.email == user.email, UserModel.id != current_user.id, UserModel.is_active.is_(True)).first()

    if existing_email:
        raise HTTPException(status_code=409, detail="Email already exists")

    current_user.name = user.name
    current_user.email = user.email
    current_user.age = user.age

    db.commit()
    db.refresh(current_user)

    return current_user


@router.patch("/", response_model=ProfileResponse, status_code=200)
def partial_update_user_profile(user: ProfilePatch, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Convierte user en un diccionario y solo incluye los campos que
    tienen un valor explicito asignado.
    """
    update_data = user.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing_email = db.query(UserModel).filter(UserModel.email == update_data["email"], UserModel.id != current_user.id, UserModel.is_active.is_(True)).first()

        if existing_email:
            raise HTTPException(status_code=409, detail="Email already exists")

    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return current_user
