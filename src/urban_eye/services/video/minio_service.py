from uuid import uuid4

from botocore.exceptions import ClientError

from urban_eye.core.minio import get_minio_client


class MinioService:
    def __init__(self):
        self.client = get_minio_client()

    async def upload_video_to_minio(self, file_bytes: bytes) -> str:
        """
        Загружает видео в MinIO и возвращает ключ
        """
        key = f"videos/{uuid4()}.mp4"

        try:
            self.client.put_object(Bucket="urban-eye", Key=key, Body=file_bytes)
        except ClientError as e:
            raise RuntimeError(f"Ошибка загрузки видео в MinIO: {e}")

        return key

    async def upload_preview_to_minio(self, preview_bytes: bytes) -> str:
        """
        Загружает превью в MinIO и возвращает ключ
        """
        key = f"previews/{uuid4()}.jpg"

        try:
            self.client.put_object(Bucket="urban-eye", Key=key, Body=preview_bytes)
        except ClientError as e:
            raise RuntimeError(f"Ошибка загрузки превью в MinIO: {e}")

        return key

    async def delete_files(self, video_key: str, preview_key: str) -> bool:
        try:
            self.client.delete_object(Bucket="urban-eye", Key=video_key)
            self.client.delete_object(Bucket="urban-eye", Key=preview_key)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] != "NoSuchKey":
                raise RuntimeError(f"Ошибка удаления файла из MinIO: {e}")
            return False

    async def download_video(self, key: str) -> bytes:
        """
        Скачивает видео из MinIO как байты
        """

        try:
            response = self.client.get_object(Bucket="urban-eye", Key=key)
            return response["Body"].read()
        except ClientError as e:
            raise RuntimeError(f"Ошибка скачивания видео из MinIO: {e}")
