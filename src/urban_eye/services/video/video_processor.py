from typing import Any, Dict

from urban_eye.services.video.metadata_extractor import extract_video_metadata
from urban_eye.services.video.minio_service import MinioServise
from urban_eye.services.video.preview_generator import generate_preview


class VideoProcessor:
    @staticmethod
    async def process_video(file_bytes: bytes) -> Dict[str, Any]:
        """
        Обрабатывает видео: загружает в MinIO, генерирует превью, извлекает метаданные.
        Возвращает информацию о видео или выбрасывает исключение при ошибке.
        """
        # Извлекаем метаданные
        try:
            metadata = extract_video_metadata(file_bytes)
        except Exception as e:
            raise RuntimeError(f"Не удалось извлечь метаданные: {e}")

        # Генерируем превью из первого кадра
        try:
            preview_bytes = generate_preview(file_bytes)

        except Exception as e:
            raise RuntimeError(f"Не удалось сгенерировать превью: {e}")

        # Сохраняем видео в MinIO
        minio_service = MinioServise()
        try:
            video_key = await minio_service.upload_video_to_minio(file_bytes)
        except Exception as e:
            raise RuntimeError(f"Не удалось загрузить видео: {e}")

        # Сохраняем превью в MinIO
        try:
            preview_key = await minio_service.upload_preview_to_minio(
                preview_bytes, "preview.jpg"
            )
        except Exception as e:
            raise RuntimeError(f"Не удалось загрузить превью: {e}")

        # Собираем результат
        return {
            "video_key": video_key,
            "preview_key": preview_key,
            "metadata": metadata,
        }
