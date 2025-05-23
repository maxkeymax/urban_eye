from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from urban_eye.core.security import get_current_user
from urban_eye.db.database import get_db
from urban_eye.repository.video import VideoCRUD
from urban_eye.schemas.video import VideoCreate, VideoResponse
from urban_eye.services.video.video_processor import VideoProcessor

router = APIRouter(prefix="/videos", tags=["Videos"])


@router.post("/upload")
async def upload_video(
    video_data: VideoCreate,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
) -> VideoResponse:
    # Начинаем обработку
    file_bytes = await file.read()

    try:
        result = await VideoProcessor.process_video(file_bytes)
        updated_data = video_data.model_dump()
        updated_data.update(
            {
                "uploader_id": current_user.id,
                "video_key": result["video_key"],
                "preview_key": result["preview_key"],
                "duration": result["metadata"]["duration_sec"],
                "fps": result["metadata"]["fps"],
                "video_resolution": result["metadata"]["video_resolution"],
            }
        )

        # Создаем объект для создания записи в БД
        video_create = VideoCreate(**updated_data)

        # Сохраняем в БД
        crud = VideoCRUD(db)
        db_video = await crud.create_video(**video_create.model_dump())

        return db_video

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при обработке видео: {str(e)}"
        )
