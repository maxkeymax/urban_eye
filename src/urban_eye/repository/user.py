from typing import Any, Optional

from sqlalchemy.future import select

from urban_eye.db.database import AsyncSession
from urban_eye.models.user import User


class UserCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db_session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def create_user(
        self,
        email: str,
        hashed_password: str,
        full_name: str,
        organization: str = None,
        is_active: bool = True,
    ) -> User:
        new_user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            organization=organization,
            is_active=is_active,
        )
        self.db_session.add(new_user)
        await self.db_session.commit()
        await self.db_session.refresh(new_user)
        return new_user

    async def update_user(
        self, user_id: int, update_data: dict[str, Any]
    ) -> Optional[User]:
        user = await self.get_by_id(user_id)
        if not user:
            return None

        for key, value in update_data.items():
            setattr(user, key, value)

        await self.db_session.commit()
        await self.db_session.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if not user:
            return False
        await self.db_session.delete(user)
        await self.db_session.commit()
        return True
