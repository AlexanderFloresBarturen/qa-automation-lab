from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.user_model import UserModel
from app.schemas import UserDetailResponse
from app.security.dependencies import require_admin

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserDetailResponse])
def get_users(current_user: UserModel = Depends(require_admin), db: Session = Depends(get_db)):
    users = db.query(UserModel).all()

    return users


@router.get("/{user_id}", response_model=UserDetailResponse, status_code=200)
def get_user(user_id: int = Path(gt=0), current_user: UserModel = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
