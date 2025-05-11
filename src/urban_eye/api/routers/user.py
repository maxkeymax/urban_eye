from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from urban_eye.db.database import get_db
from urban_eye.models.user import User
from urban_eye.repository.user import UserCRUD

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=User)
async def create_user(
    email: str, hashed_password: str, full_name: str, db: AsyncSession = Depends(get_db)
) -> User:
    crud = UserCRUD(db)
    try:
        return await crud.create_user(
            email=email, hashed_password=hashed_password, full_name=full_name
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Такая почта уже зарегистрирована")


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> User:
    crud = UserCRUD(db)
    user = await crud.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.put('/{user_id}', response_model=User)
async def update_user(
    user_id: int,
    email: str = None,
    hashed_password: str = None,
    full_name: str = None,
    organization: str = None,
    is_active: bool = None,
    db: AsyncSession = Depends(get_db)
) -> User:
    crud = UserCRUD(db)
    updated = await crud.update_user(
        user_id=user_id,
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        organization=organization,
        is_active=is_active
    )
    if not updated:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return updated


@router.delete('/{user_id}')
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    crud = UserCRUD(db)
    deleted = await crud.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return {'detail': 'Пользователь успешно удален'}
