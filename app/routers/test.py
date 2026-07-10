from fastapi import APIRouter, Depends

from app.models.user_model import UserModel
from app.schemas.user import UserResponse
from app.security.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/tests", tags=["Tests"])


@router.get("/me", response_model=UserResponse)
def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


@router.get("/admin")
def admin_endpoint(current_user: UserModel = Depends(require_admin)):
    return {"message": "Admin access granted"}
