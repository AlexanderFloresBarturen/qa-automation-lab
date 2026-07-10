from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.user_model import UserModel
from app.security.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserModel:
    try:
        user_id = decode_access_token(token)

    except Exception:
        raise credentials_exception

    user = db.query(UserModel).filter(UserModel.id == user_id, UserModel.is_active.is_(True)).first()

    if not user:
        raise credentials_exception

    return user


def require_admin(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    if current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return current_user
