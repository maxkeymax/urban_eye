from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from urban_eye.core.security import get_current_user
from urban_eye.db.database import get_db
from urban_eye.models.user import User
from urban_eye.repository.video import VideoCRUD
from urban_eye.schemas.video import VideoResponse, VideoUpdate
from urban_eye.services.video.video_upload_service import VideoUploadService

router = APIRouter(prefix="/videos", tags=["Videos"])


@router.post("/upload", response_model=VideoResponse)
async def upload_video(
    title: str = Form(..., min_length=1, max_length=255),
    time_of_day: str = Form(..., pattern="утро|день|вечер|ночь"),
    camera_id: str = Form(
        ..., regex=r"^[0-9a-f-]{36}$", examples=["0321e13a-6a7e-4bde-87d2-5f2d39152831"]
    ),  # UUID
    status: str = Form(default="processing"),
    file: UploadFile = File(...),
    uploader: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> VideoResponse:
    service = VideoUploadService(db)
    return await service.upload_raw_video(
        file, title, time_of_day, camera_id, uploader.id
    )


@router.get("/", response_model=List[VideoResponse])
async def get_user_videos(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[VideoResponse]:
    crud = VideoCRUD(db)
    videos = await crud.get_videos(current_user.id)

    if not videos:
        raise HTTPException(status_code=404, detail="Видео не найдены")

    return videos


@router.put("/{video_id}", response_model=VideoResponse)
async def update_video(
    video_id: int,
    data: VideoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> VideoResponse:
    crud = VideoCRUD(db)
    updated = await crud.update_video(
        video_id=video_id, update_data=data.model_dump(exclude_unset=True)
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Видео не найдено")
    return updated


@router.delete("/{video_id}")
async def delete_video(
    video_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    crud = VideoCRUD(db)
    deleted = await crud.delete_video(video_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Видео не найдено")
    return {"detail": "Видео успешно удалено"}
