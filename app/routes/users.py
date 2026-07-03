from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets

from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserPatch, LoginResponse, ForgotPasswordRequest, ForgotPasswordResponse, ResetPasswordRequest, ResetPasswordResponse
from app.database.dependencies import get_db
from app.models.user_model import UserModel
from app.models.role_model import RoleModel
from app.models.token_model import PasswordResetTokenModel
from app.security.password import hash_password, verify_password
from app.security.jwt import create_access_token
from app.security.dependencies import get_current_user, require_admin
from app.services.email_service import send_password_reset_email
from app.core.settings import settings

router = APIRouter()


# region register_user
@router.post("/", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Consultar si existe un usuario con ese correo
    existing_user = db.query(UserModel).filter(UserModel.email == user.email, UserModel.is_active.is_(True)).first()

    if existing_user:
        raise HTTPException(status_code=409, detail="Email already exists")

    user_role = db.query(RoleModel).filter(RoleModel.name == "user").first()

    # Registrar el usuario
    new_user = UserModel(name=user.name, email=user.email, age=user.age, password_hash=hash_password(user.password), role_id=user_role.id)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# endregion


# region get_user
@router.get("/{user_id}", response_model=UserResponse, status_code=200)
def get_user(user_id: int = Path(gt=0), current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return current_user


# endregion


# region get_users
@router.get("/", response_model=list[UserResponse])
def get_users(current_user: UserModel = Depends(require_admin), db: Session = Depends(get_db)):
    users = db.query(UserModel).filter(UserModel.is_active.is_(True)).all()

    return users


# endregion


# region delete_user
@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int = Path(gt=0), current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    current_user.is_active = False

    db.commit()

    return


# endregion


# region update_user
@router.put("/{user_id}", response_model=UserResponse, status_code=200)
def update_user(user: UserUpdate, user_id: int = Path(..., gt=0), current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    existing_email = db.query(UserModel).filter(UserModel.email == user.email, UserModel.id != user_id, UserModel.is_active.is_(True)).first()

    if existing_email:
        raise HTTPException(status_code=409, detail="Email already exists")

    current_user.name = user.name
    current_user.email = user.email
    current_user.age = user.age

    db.commit()
    db.refresh(current_user)

    return current_user


# endregion


# region partial_update_user
@router.patch("/{user_id}", response_model=UserResponse, status_code=200)
def partial_update_user(user: UserPatch, user_id: int = Path(..., gt=0), current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

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
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return current_user


# endregion


# region login
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


# endregion


# region Recuperación de contraseña
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


# endregion


# region endpoints de prueba
# JWT
@router.get("/test/me", response_model=UserResponse)
def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


# rol admin
@router.get("/test/admin")
def admin_endpoint(current_user: UserModel = Depends(require_admin)):
    return {"message": "Admin access granted"}


# endregion
