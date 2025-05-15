# models.py

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from urban_eye.db.base import Base

from .camera import Camera
from .user import User


class Video(Base):
    __tablename__ = 'videos'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    # Ключи в MinIO
    video_key: Mapped[str] = mapped_column(String(255), nullable=False)
    preview_key: Mapped[str] = mapped_column(String(255))  # Ключ превью в MinIO

    # Метаданные видео
    duration: Mapped[int] = mapped_column(Integer, nullable=False)  # секунды
    video_resolution: Mapped[str] = mapped_column(String(20), nullable=False)  # например "1920x1080"
    fps: Mapped[int] = mapped_column(Integer, nullable=False)
    time_of_day: Mapped[str] = mapped_column(
        String(10), nullable=False, 
        comment='Время суток: утро, день, вечер, ночь')  # время создания видео

    # Автор и камера
    uploader_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    camera_id: Mapped[int] = mapped_column(ForeignKey("cameras.id"))

    # Отношения
    uploader: Mapped["User"] = relationship(back_populates="videos")
    camera: Mapped["Camera"] = relationship(back_populates="videos")

    # Время загрузки в систему
    uploaded_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Статус готовности видео
    status: Mapped[str] = mapped_column(String(20), default="processing")  # "processing", "ready"
    