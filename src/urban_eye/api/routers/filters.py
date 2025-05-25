from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from urban_eye.core.security import get_current_user
from urban_eye.db.database import get_db
from urban_eye.models.user import User
from urban_eye.repository.user import UserCRUD
from urban_eye.repository.video import VideoCRUD
from urban_eye.schemas.filters import UserFiltersResponse, VideoFiltersResponse

router = APIRouter(prefix="/filters", tags=["Filters"])


@router.get("/video_filters", response_model=VideoFiltersResponse)
async def get_video_filters(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
) -> VideoFiltersResponse:
    crud = VideoCRUD(db)
    video_filters = await crud.get_filters()

    if not video_filters:
        raise HTTPException(status_code=404, detail="Нет загруженных видео")

    return video_filters


@router.get("/full_names", response_model=UserFiltersResponse)
async def get_user_full_names(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
) -> UserFiltersResponse:
    crud = UserCRUD(db)
    names = await crud.get_user_full_names()
    return UserFiltersResponse(full_names=names)
