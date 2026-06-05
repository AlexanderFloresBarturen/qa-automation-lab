from fastapi import APIRouter

from app.schemas import UserCreate

router = APIRouter()

@router.post("")
def register_user(
    user: UserCreate
):
    return {"message": "User received"}