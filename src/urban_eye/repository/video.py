from typing import Optional

from sqlalchemy.future import select

from urban_eye.db.database import AsyncSession
from urban_eye.models.video import Video


class VideoCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_id(self, video_id: int) -> Optional[Video]:
        result = await self.db_session.execute(
            select(Video).where(Video.id == video_id)
        )
        return result.scalars().first()

    async def create_video(
        db: AsyncSession,
        uploader_id: int,
        video_key: str,
        preview_key: str,
        fps: float,
        duration_sec: float,
        video_resolution: str,
    ):
        """
        Сохраняет информацию о видео в БД
        """
        new_video = Video(
            uploader_id=uploader_id,
            video_key=video_key,
            preview_key=preview_key,
            fps=fps,
            duration_sec=duration_sec,
            video_resolution=video_resolution,
        )
        db.add(new_video)
        await db.commit()
        await db.refresh(new_video)

        return new_video

    # async def update_video(
    #     self, video_id: int, update_data: dict[str, Any]
    # ) -> Optional[Video]:
    #     video = await self.get_by_id(video_id)
    #     if not video:
    #         return None

    #     for key, value in update_data.items():
    #         setattr(video, key, value)

    #     await self.db_session.commit()
    #     await self.db_session.refresh(video)
    #     return video

    # async def delete_video(self, video_id: int) -> bool:
    #     video = await self.get_by_id(video_id)
    #     if not video:
    #         return False
    #     await self.db_session.delete(video)
    #     await self.db_session.commit()
    #     return True
