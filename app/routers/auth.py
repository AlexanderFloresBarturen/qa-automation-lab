import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.database.dependencies import get_db
from app.models.role_model import RoleModel
from app.models.token_model import PasswordResetTokenModel
from app.models.user_model import UserModel
from app.schemas import LoginResponse, RegisterRequest, RegisterResponse, ForgotPasswordRequest, ForgotPasswordResponse, ResetPasswordRequest, ResetPasswordResponse
from app.security.jwt import create_access_token
from app.security.password import hash_password, verify_password
from app.services.email_service import send_password_reset_email

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


@router.post("/register", response_model=RegisterResponse, status_code=201)
def register_user(user: RegisterRequest, db: Session = Depends(get_db)):
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


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == request.email, UserModel.is_active.is_(True)).first()

    if not existing_user:
        return {"message": "If the account exists, a recovery token has been generated"}

    active_tokens = db.query(PasswordResetTokenModel).filter(PasswordResetTokenModel.user_id == existing_user.id, PasswordResetTokenModel.used.is_(False)).all()

    for token in active_tokens:
        token.used = True

    new_token = secrets.token_urlsafe(32)

    reset_token = PasswordResetTokenModel(
        user_id=existing_user.id, token=new_token, used=False, created_at=datetime.now(), expires_at=datetime.now() + timedelta(minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES)
    )

    db.add(reset_token)
    db.commit()

    try:
        email_sent = send_password_reset_email(email=existing_user.email, token=new_token)
    except Exception:
        raise HTTPException(status_code=500, detail="Email service unavailable")

    if not email_sent:
        raise HTTPException(status_code=500, detail="Email service unavailable")

    return {"message": "Recovery token generated", "token": new_token}


@router.post("/reset-password", response_model=ResetPasswordResponse)
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    reset_token = db.query(PasswordResetTokenModel).filter(PasswordResetTokenModel.token == request.token).first()

    if not reset_token or reset_token.used or reset_token.expires_at < datetime.now():
        raise HTTPException(status_code=400, detail="Invalid token")

    user = reset_token.user

    user.password_hash = hash_password(request.new_password)

    user.failed_login_attempts = 0
    user.locked_until = None

    reset_token.used = True

    db.commit()

    return {"message": "Password successfully reset"}
