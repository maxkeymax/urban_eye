from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from urban_eye.repository.video import VideoCRUD
from urban_eye.services.video.minio_service import MinioService
from urban_eye.tasks.video_tasks import process_video_task


class VideoUploadService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.crud = VideoCRUD(db)
        self.minio_service = MinioService()

    async def upload_raw_video(
        self, file, title: str, time_of_day: str, camera_id: str, uploader_id: int
    ):
        if not file.filename.endswith(".mp4"):
            raise HTTPException(status_code=400, detail="Формат файла должен быть .mp4")

        file_bytes = file.file.read()
        remote_video_key = await self.minio_service.upload_video_to_minio(file_bytes)

        db_video = await self.crud.create_video(
            title=title,
            time_of_day=time_of_day,
            camera_id=camera_id,
            uploader_id=uploader_id,
            video_key=remote_video_key,
            status="processing",
            preview_key="",
            fps=0,
            duration=0,
            video_resolution="0x0",
        )
        process_video_task.delay(video_id=db_video.id)

        return db_video
