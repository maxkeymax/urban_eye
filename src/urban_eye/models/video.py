
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from urban_eye.db.base import Base

from .camera import Camera
from .user import User


class Video(Base):
    __tablename__ = 'videos'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)

    uploader_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    camera_id: Mapped[int] = mapped_column(ForeignKey("cameras.id"))

    uploader: Mapped["User"] = relationship(back_populates="videos")
    camera: Mapped["Camera"] = relationship(back_populates="videos")