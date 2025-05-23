from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class VideoBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        examples=["Видео с камеры 1"],
        description="Название видео",
    )
    
    time_of_day: str = Field(
        ...,
        examples=["утро", "день", "вечер", "ночь"],
        description="Время суток создания видео",
    )


class VideoCreate(VideoBase):
    # uploader_id: int = Field(..., examples=[1])
    camera_id: int = Field(..., examples=[1])
    status: str = Field(default="processing", examples=["processing", "ready"])


class VideoResponse(VideoBase):
    id: int = Field(examples=[1])
    uploaded_at: datetime = Field(examples=["2024-03-20T12:00:00+03:00"])
    uploader_id: int = Field(examples=[1])
    camera_id: int = Field(examples=[1])
    status: str = Field(examples=["processing", "ready"])
    video_key: str = Field(ё
        max_length=255,
        examples=["videos/2024/03/20/1.mp4"],
        description="Ключ видео в MinIO или другом хранилище",
    )
    preview_key: Optional[str] = Field(
        default=None,
        max_length=255,
        examples=["previews/2024/03/20/1.jpg"],
        description="Ключ превью к видео в MinIO ",
    )
    duration: int = Field(
        ...,
        ge=1,
        examples=[3600],
        description="Длительность видео в секундах",
    )
    video_resolution: str = Field(
        ...,
        examples=["1920x1080", "1280x720"],
        pattern=r"^\d+x\d+$",
        description="Разрешение видео в формате ШИРИНАxВЫСОТА",
    )
    fps: int = Field(
        ...,
        ge=1,
        examples=[30],
        description="Частота кадров в секунду",
    )

    model_config = ConfigDict(from_attributes=True)


class VideoUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        examples=["Видео с камеры 1"],
        description="Название видео",
    )
    video_key: Optional[str] = Field(
        default=None,
        max_length=255,
        examples=["videos/2024/03/20/1.mp4"],
        description="Ключ видео в MinIO или другом хранилище",
    )
    preview_key: Optional[str] = Field(
        default=None,
        max_length=255,
        examples=["previews/2024/03/20/1.jpg"],
        description="Ключ превью к видео",
    )
    duration: Optional[int] = Field(
        default=None,
        ge=1,
        examples=[3600],
        description="Длительность видео в секундах",
    )
    video_resolution: Optional[str] = Field(
        default=None,
        examples=["1920x1080", "1280x720"],
        pattern=r"^\d+x\d+$",
        description="Разрешение видео в формате ШИРИНАxВЫСОТА",
    )
    fps: Optional[int] = Field(
        default=None,
        examples=[30],
        description="Частота кадров в секунду",
    )
    time_of_day: Optional[datetime] = Field(
        default=None,
        examples=["2024-03-20T12:00:00+03:00"],
        description="Время записи видео",
    )
    status: Optional[str] = Field(
        default=None, examples=["processing", "ready"], description="Статус видео"
    )

    model_config = ConfigDict(validate_assignment=True)
