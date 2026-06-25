from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from app.core.settings import settings

def create_access_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise ValueError("Missing subject")
        
        return int(user_id)
    
    except (JWTError, ValueError) as exc:
        raise ValueError("Could not validate credentials") from exc