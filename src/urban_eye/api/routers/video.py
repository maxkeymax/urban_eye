from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from urban_eye.core.security import get_current_user
from urban_eye.db.database import get_db
from urban_eye.models.user import User
from urban_eye.repository.video import VideoCRUD
from urban_eye.schemas.video import VideoResponse
from urban_eye.services.video.video_processor import VideoProcessor

router = APIRouter(prefix="/videos", tags=["Videos"])


@router.post("/upload", response_model=VideoResponse)
async def upload_video(
    # Поля из VideoCreate (разбираем вручную)
    title: str = Form(..., min_length=1, max_length=255),
    time_of_day: str = Form(..., pattern="утро|день|вечер|ночь"),
    camera_id: str = Form(
        ..., regex=r"^[0-9a-f-]{36}$", examples=["5e31ca75-0237-4ce1-81b8-1069fc764047"]
    ),  # UUID
    status: str = Form(default="processing"),
    file: UploadFile = File(...),
    uploader: int = Depends(
        get_current_user
    ),  # Пока хардкод, потом заменить на Depends
    db: AsyncSession = Depends(get_db),
) -> VideoResponse:
    # Собираем все данные в словарь
    video_data = {
        "title": title,
        "time_of_day": time_of_day,
        "camera_id": camera_id,
        "status": status,
        "uploader_id": uploader.id,
    }

    # Обработка видео
    file_bytes = await file.read()
    result = await VideoProcessor.process_video(file_bytes)

    # Объединяем данные
    full_data = {
        **video_data,
        "video_key": result["video_key"],
        "preview_key": result["preview_key"],
        "duration": result["metadata"]["duration_sec"],
        "fps": result["metadata"]["fps"],
        "video_resolution": result["metadata"]["video_resolution"],
    }

    # Сохраняем в БД
    crud = VideoCRUD(db)
    db_video = await crud.create_video(**full_data)

    return db_video


@router.get("/videos", response_model=List[VideoResponse])
async def get_user_videos(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[VideoResponse]:
    crud = VideoCRUD(db)
    videos = await crud.get_videos(current_user.id)

    if not videos:
        raise HTTPException(status_code=404, detail="Видео не найдены")

    return videos
