from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from urban_eye.db.base import Base

if TYPE_CHECKING:
    from urban_eye.models.video import Video


class Camera(Base):
    __tablename__ = "cameras"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    videos: Mapped[List["Video"]] = relationship(back_populates="camera")
