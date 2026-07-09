from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.database.dependencies import get_db
from app.models.role_model import RoleModel
from app.models.user_model import UserModel
from app.schemas.user import LoginResponse, UserResponse, UserCreate
from app.security.jwt import create_access_token
from app.security.password import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == form_data.username, UserModel.is_active.is_(True)).first()

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if existing_user.locked_until is not None and existing_user.locked_until > datetime.now():
        raise HTTPException(status_code=423, detail="Account locked")

    if existing_user.locked_until is not None and existing_user.locked_until <= datetime.now():
        existing_user.failed_login_attempts = 0
        existing_user.locked_until = None
        db.commit()

    if not verify_password(form_data.password, existing_user.password_hash):
        existing_user.failed_login_attempts += 1

        if existing_user.failed_login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
            existing_user.locked_until = datetime.now() + timedelta(minutes=settings.ACCOUNT_LOCK_MINUTES)

        db.commit()

        if existing_user.failed_login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
            raise HTTPException(status_code=423, detail="Account locked")
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")

    existing_user.failed_login_attempts = 0
    existing_user.locked_until = None

    db.commit()

    access_token = create_access_token(existing_user.id)

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
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