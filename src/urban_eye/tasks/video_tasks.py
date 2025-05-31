import asyncio
import random
from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from urban_eye.core.celery_app import celery_app
from urban_eye.db.database import AsyncSessionLocal
from urban_eye.repository.video import VideoCRUD
from urban_eye.services.video.metadata_extractor import extract_video_metadata
from urban_eye.services.video.minio_service import MinioService
from urban_eye.services.video.preview_generator import generate_preview


@celery_app.task(name="process_video_task")
def process_video_task(video_id: int) -> Dict[str, Any]:
    try:
        # Пытаемся получить существующий event loop
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # Если loop не существует, создаем новый
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Проверяем, не закрыт ли loop
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    async def wrapper():
        async with AsyncSessionLocal() as db:
            return await process_video(video_id, db)

    try:
        return loop.run_until_complete(wrapper())
    except Exception as e:
        # В случае ошибки логируем и пытаемся создать новый loop
        print(f"Ошибка в задаче обработки видео: {str(e)}")
        loop.close()
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        return new_loop.run_until_complete(wrapper())


async def process_video(video_id: int, db: AsyncSession) -> Dict[str, Any]:
    """
    Асинхронная обработка видео:
    1. Получает видео из БД
    2. Скачивает из MinIO
    3. Извлекает метаданные
    4. Генерирует превью
    5. Обновляет запись в БД
    """

    crud = VideoCRUD(db)
    minio_service = MinioService()

    # 1. Получаем видео по ID
    video = await crud.get_by_id(video_id)
    if not video:
        error_msg = f"Видео {video_id} не найдено"
        print(error_msg)
        return {"status": "error", "message": error_msg}

    try:
        # 2. Скачиваем видео из MinIO
        video_bytes = await minio_service.download_video(video.video_key)

        # 3. Извлекаем метаданные
        metadata = extract_video_metadata(video_bytes)

        # 4. Генерируем превью
        preview_bytes = generate_preview(video_bytes)

        # 5. Загружаем превью в MinIO
        preview_key = await minio_service.upload_preview_to_minio(preview_bytes)

        # 6. Обновляем запись в БД
        update_data = {
            "status": "ready",
            "fps": metadata["fps"],
            "duration": metadata["duration_sec"],
            "video_resolution": metadata["video_resolution"],
            "preview_key": preview_key,
        }

        updated_video = await crud.update_video(video_id, update_data)

        # Преобразуем SQLAlchemy модель в словарь для сериализации
        video_data = {
            "id": updated_video.id,
            "title": updated_video.title,
            "status": updated_video.status,
            "preview_key": updated_video.preview_key,
            "duration": updated_video.duration,
            "video_resolution": updated_video.video_resolution,
            "fps": updated_video.fps,
        }

        print(f"Видео {video_id} успешно обработано")
        return {
            "status": "success",
            "video_id": video_id,
            "video": video_data,
            "message": "Video processed successfully",
        }

    except Exception as e:
        error_msg = f"Ошибка при обработке видео {video_id}: {str(e)}"
        print(error_msg)

        # Пытаемся обновить статус в БД даже при ошибке
        try:
            await crud.update_video(video_id, {"status": "failed"})
        except Exception as db_error:
            print(f"Не удалось обновить статус видео: {str(db_error)}")

        return {
            "status": "error",
            "video_id": video_id,
            "error": str(e),
            "message": error_msg,
        }
