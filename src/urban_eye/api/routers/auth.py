from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from urban_eye.core.security import Hashing
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
