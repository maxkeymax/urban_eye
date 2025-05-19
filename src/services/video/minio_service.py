from uuid import uuid4

from botocore.exceptions import ClientError

from urban_eye.core.minio import get_minio_client


class MinioServise:
    async def upload_video_to_minio(file_bytes: bytes) -> str:
        """
        Загружает видео в MinIO и возвращает ключ
        """
        client = get_minio_client()
        key = f"videos/{uuid4()}.mp4"

        try:
            client.put_object(Bucket="urban-eye", Key=key, Body=file_bytes)
        except ClientError as e:
            raise RuntimeError(f"Ошибка загрузки видео в MinIO: {e}")

        return key

    async def upload_preview_to_minio(preview_bytes: bytes, filename: str) -> str:
        """
        Загружает превью в MinIO и возвращает ключ
        """
        client = get_minio_client()
        key = f"previews/{uuid4()}.jpg"

        try:
            client.put_object(Bucket="urban-eye", Key=key, Body=preview_bytes)
        except ClientError as e:
            raise RuntimeError(f"Ошибка загрузки превью в MinIO: {e}")

        return key
