# urban_eye/models/camera.py

import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from urban_eye.db.base import Base

if TYPE_CHECKING:
    from urban_eye.models.video import Video


class Camera(Base):
    __tablename__ = "cameras"

    id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    camera_id: Mapped[str] = mapped_column(String(50), nullable=False)  # Номер камеры
    camera_class_cd: Mapped[int] = mapped_column(Integer, nullable=False)  # ID класса камеры
    camera_class: Mapped[str] = mapped_column(String(100), nullable=False)  # Класс камеры
    model: Mapped[str] = mapped_column(String(100))  # Модель камеры
    camera_name: Mapped[str] = mapped_column(String(255), nullable=False)  # Название камеры
    camera_place: Mapped[str] = mapped_column(String(255))  # Адрес
    camera_place_cd: Mapped[int] = mapped_column(Integer)  # ID адреса
    serial_number: Mapped[str] = mapped_column(String(100))  # Серийный номер
    camera_type_cd: Mapped[int] = mapped_column(Integer, nullable=False)  # ID типа камеры
    camera_type: Mapped[str] = mapped_column(String(100), nullable=False)  # Тип камеры
    camera_latitude: Mapped[float] = mapped_column(Float)  # Широта
    camera_longitude: Mapped[float] = mapped_column(Float)  # Долгота
    archive: Mapped[bool] = mapped_column(Boolean, default=False)  # Признак архива (tinyint → bool)
    azimuth: Mapped[int] = mapped_column(Integer)  # Азимут
    process_dttm: Mapped[DateTime] = mapped_column(DateTime, nullable=False)  # Время добавления записи

    # Связь с видео
    videos: Mapped[List["Video"]] = relationship(back_populates="camera")
    