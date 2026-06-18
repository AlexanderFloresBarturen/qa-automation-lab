from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.schemas import UserCreate, UserResponse, UserUpdate, UserPatch, LoginRequest, LoginResponse
from app.dependencies import get_db
from app.models import UserModel
from app.security.password import hash_password, verify_password
from app.security.jwt import create_access_token
from app.security.dependencies import get_current_user

router = APIRouter()

#region register_user
@router.post("/", response_model=UserResponse, status_code=201)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    # Consultar si existe un usuario con ese correo
    existing_user = db.query(UserModel).filter(
        UserModel.email == user.email,
        UserModel.is_active.is_(True)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code = 409,
            detail = "Email already exists"
        )
    
    # Registrar el usuario
    new_user = UserModel(
        name = user.name,
        email = user.email,
        age = user.age,
        password_hash = hash_password(user.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#endregion

#region get_user
@router.get("/{user_id}", response_model=UserResponse, status_code=200)
def get_user(
    user_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(
        UserModel.id == user_id,
        UserModel.is_active.is_(True)
    ).first()

    if not user:
        raise HTTPException(
            status_code = 404,
            detail = "User not found"
        )
    
    return user

#endregion

#region delete_user
@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(
        UserModel.id == user_id,
        UserModel.is_active.is_(True)
    ).first()

    if not user:
        raise HTTPException(
            status_code = 404,
            detail = "User not found"
        )
    
    user.is_active = False

    db.commit()

    return

#endregion

#region update_user
@router.put("/{user_id}", response_model=UserResponse, status_code=200)
def update_user(
    user: UserUpdate,
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    user_to_update = db.query(UserModel).filter(
        UserModel.id == user_id,
        UserModel.is_active.is_(True)
    ).first()

    if not user_to_update:
        raise HTTPException(
            status_code = 404,
            detail = "User not found"
        )
    
    existing_email = db.query(UserModel).filter(
        UserModel.email == user.email,
        UserModel.id != user_id,
        UserModel.is_active.is_(True)
    ).first()

    if existing_email:
        raise HTTPException(
            status_code = 409,
            detail = "Email already exists"
        )
    
    user_to_update.name = user.name
    user_to_update.email = user.email
    user_to_update.age = user.age

    db.commit()
    db.refresh(user_to_update)

    return user_to_update

#endregion

#region partial_update_user
@router.patch("/{user_id}", response_model=UserResponse, status_code=200)
def partial_update_user(
    user: UserPatch,
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    user_to_update = db.query(UserModel).filter(
        UserModel.id == user_id,
        UserModel.is_active.is_(True)
    ).first()

    if not user_to_update:
        raise HTTPException(
            status_code = 404,
            detail = "User not found"
        )
    
    """
    Convierte user en un diccionario y solo incluye los campos que 
    tienen un valor explicito asignado.
    """
    update_data = user.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing_email = db.query(UserModel).filter(
            UserModel.email == update_data["email"],
            UserModel.id != user_id,
            UserModel.is_active.is_(True)
        ).first()

        if existing_email:
            raise HTTPException(
                status_code = 409,
                detail = "Email already exists"
            )
    
    for field, value in update_data.items():
        setattr(user_to_update, field, value)
    
    db.commit()
    db.refresh(user_to_update)

    return user_to_update

#endregion

#region login
@router.post("/login", response_model=LoginResponse)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    existing_user = db.query(UserModel).filter(
        UserModel.email == credentials.email,
        UserModel.is_active.is_(True)
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code= 401,
            detail= "Invalid credentials"
        )
    
    if not verify_password(
        credentials.password,
        existing_user.password_hash
    ):
        raise HTTPException(
            status_code= 401,
            detail= "Invalid credentials"
        )
    
    access_token = create_access_token(existing_user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

#endregion

#region endpoint de prueba JWT
@router.get("/test/me", response_model=UserResponse)
def get_me(
    current_user: UserModel = Depends(get_current_user)
):
    return current_user

#endregion