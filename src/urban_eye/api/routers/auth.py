from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from urban_eye.core.security import Hashing, TokenGenerator
from urban_eye.db.database import get_db
from urban_eye.repository.user import UserCRUD
from urban_eye.schemas.user import UserCreate

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> dict:
    user_crud = UserCRUD(db)

    existing_user = await user_crud.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует",
        )
    hashed_password = Hashing.get_password_hash(user_data.password)

    new_user = await user_crud.create_user(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        organization=user_data.organization,
    )

    return {
        "message": "Регистрация прошла успешно",
        "user_id": new_user.id,
        "email": new_user.email,
    }


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
) -> dict:
    user_crud = UserCRUD(db)
    user = await user_crud.get_by_email(form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = TokenGenerator.create_access_token(data={"sub": str(user.id)})
    refresh_token = TokenGenerator.create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
