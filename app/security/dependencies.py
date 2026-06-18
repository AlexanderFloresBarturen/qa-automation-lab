from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import UserModel
from app.security.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserModel:
    try:
        user_id = decode_access_token(token)
    
    except Exception:
        raise credentials_exception
    
    user = db.query(UserModel).filter(
        UserModel.id == user_id,
        UserModel.is_active.is_(True)
    ).first()

    if not user:
        raise credentials_exception
    
    return user