from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.role_model import RoleModel
from app.models.user_model import UserModel
from app.schemas.user import CreateUserRequest, PatchUserRequest, UpdateUserRequest, UserDetailResponse, UserStatusRequest
from app.security.dependencies import require_admin
from app.security.password import hash_password

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserDetailResponse])
def get_users(_: UserModel = Depends(require_admin), db: Session = Depends(get_db)):
    users = db.query(UserModel).order_by(UserModel.id).all()

    return users


@router.get("/{user_id}", response_model=UserDetailResponse, status_code=200)
def get_user(user_id: int = Path(gt=0), _: UserModel = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/", response_model=UserDetailResponse, status_code=201)
def create_user(user: CreateUserRequest, _: UserModel = Depends(require_admin), db: Session = Depends(get_db)):
    # Consultar si existe un usuario con ese correo
    existing_user = db.query(UserModel).filter(UserModel.email == user.email, UserModel.is_active.is_(True)).first()

    if existing_user:
        raise HTTPException(status_code=409, detail="Email already exists")

    user_role = db.query(RoleModel).filter(RoleModel.name == "user").first()

    # Registrar el usuario
    if user_role is None:
        raise RuntimeError("Default role 'user' not found. Verify database migrations.")

    new_user = UserModel(name=user.name, email=user.email, age=user.age, password_hash=hash_password(user.password), role_id=user_role.id)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.put("/{user_id}", response_model=UserDetailResponse, status_code=200)
def update_user(user: UpdateUserRequest, user_id: int = Path(gt=0), _: UserModel = Depends(require_admin), db: Session = Depends(get_db)):
    user_to_update = db.query(UserModel).filter(UserModel.id == user_id, UserModel.is_active.is_(True)).first()

    if user_to_update is None:
        raise HTTPException(status_code=404, detail="User not found")

    existing_email = db.query(UserModel).filter(UserModel.email == user.email, UserModel.id != user_id, UserModel.is_active.is_(True)).first()

    if existing_email:
        raise HTTPException(status_code=409, detail="Email already exists")

    user_to_update.name = user.name
    user_to_update.email = user.email
    user_to_update.age = user.age

    db.commit()
    db.refresh(user_to_update)

    return user_to_update


@router.patch("/{user_id}", response_model=UserDetailResponse, status_code=200)
def partial_update_user(user: PatchUserRequest, user_id: int = Path(gt=0), _: UserModel = Depends(require_admin), db: Session = Depends(get_db)):
    user_to_update = db.query(UserModel).filter(UserModel.id == user_id, UserModel.is_active.is_(True)).first()

    if user_to_update is None:
        raise HTTPException(status_code=404, detail="User not found")

    """
    Convierte user en un diccionario y solo incluye los campos que
    tienen un valor explicito asignado.
    """
    update_data = user.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing_email = db.query(UserModel).filter(UserModel.email == update_data["email"], UserModel.id != user_id, UserModel.is_active.is_(True)).first()

        if existing_email:
            raise HTTPException(status_code=409, detail="Email already exists")

    for field, value in update_data.items():
        setattr(user_to_update, field, value)

    db.commit()
    db.refresh(user_to_update)

    return user_to_update


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int = Path(gt=0), current_user: UserModel = Depends(require_admin), db: Session = Depends(get_db)):
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Use DELETE /profile to delete your own account.")

    user_to_delete = db.query(UserModel).filter(UserModel.id == user_id, UserModel.is_active.is_(True)).first()

    if user_to_delete is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_to_delete.is_active = False

    db.commit()

    return


@router.patch("/{user_id}/status", response_model=UserDetailResponse, status_code=200)
def update_user_status(status: UserStatusRequest, user_id: int = Path(gt=0), _: UserModel = Depends(require_admin), db: Session = Depends(get_db)):
    user_to_update = db.query(UserModel).filter(UserModel.id == user_id, UserModel.is_active.is_(False)).first()

    if user_to_update is None:
        raise HTTPException(status_code=404, detail="User not found")

    if status.is_active is False:
        raise HTTPException(status_code=409, detail="User already deactivated")

    user_to_update.is_active = status.is_active

    db.commit()
    db.refresh(user_to_update)

    return user_to_update
