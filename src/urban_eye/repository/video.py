import uuid
from typing import Any, List, Optional

from sqlalchemy import distinct, func
from sqlalchemy.future import select

from urban_eye.db.database import AsyncSession
from urban_eye.models.video import Video
from urban_eye.schemas.filters import DateRange, DurationRange, VideoFiltersResponse


class VideoCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_id(self, video_id: int) -> Optional[Video]:
        result = await self.db_session.execute(
            select(Video).where(Video.id == video_id)
        )
        return result.scalars().first()

    async def create_video(
        self,
        title: str,
        time_of_day: str,
        camera_id: uuid.UUID,
        status: str,
        uploader_id: int,
        video_key: str,
        preview_key: str,
        fps: float,
        duration: int,
        video_resolution: str,
    ):
        """
        Сохраняет информацию о видео в БД
        """
        new_video = Video(
            title=title,
            time_of_day=time_of_day,
            camera_id=camera_id,
            status=status,
            uploader_id=uploader_id,
            video_key=video_key,
            preview_key=preview_key,
            fps=fps,
            duration=duration,
            video_resolution=video_resolution,
        )
        self.db_session.add(new_video)
        await self.db_session.commit()
        await self.db_session.refresh(new_video)

        return new_video

    async def get_videos(
        self,
        user_id: int,
        limit: int = 5,
    ) -> List[Video]:
        result = await self.db_session.execute(
            select(Video).where(Video.uploader_id == user_id).limit(limit)
        )
        return result.scalars().all()

    async def get_filters(self) -> VideoFiltersResponse:
        querry = select(
            func.min(Video.uploaded_at).label("min_upload_date"),
            func.max(Video.uploaded_at).label("max_upload_date"),
            func.min(Video.duration).label("min_duration"),
            func.max(Video.duration).label("max_duration"),
            func.array_agg(distinct(Video.time_of_day)).label("distinct_times_of_day"),
            func.array_agg(distinct(Video.status)).label("distinct_statuses"),
        )

        result = await self.db_session.execute(querry)
        filters_data = result.fetchone()

        if not filters_data.min_upload_date:
            return VideoFiltersResponse(
                upload_date=DateRange(min=None, max=None),
                duration=DurationRange(min=None, max=None),
                time_of_day=[],
                status=[],
            )
        return VideoFiltersResponse(
            upload_date=DateRange(
                min=filters_data.min_upload_date.isoformat(),
                max=filters_data.max_upload_date.isoformat(),
            ),
            duration=DurationRange(
                min=filters_data.min_duration,
                max=filters_data.max_duration,
            ),
            time_of_day=list(set(filters_data.distinct_times_of_day)),
            status=list(set(filters_data.distinct_statuses)),
        )

    async def update_video(
        self, video_id: int, update_data: dict[str, Any]
    ) -> Optional[Video]:
        video = await self.get_by_id(video_id)
        if not video:
            return None

        for key, value in update_data.items():
            setattr(video, key, value)

        await self.db_session.commit()
        await self.db_session.refresh(video)
        return video

    # async def delete_video(self, video_id: int) -> bool:
    #     video = await self.get_by_id(video_id)
    #     if not video:
    #         return False
    #     await self.db_session.delete(video)
    #     await self.db_session.commit()
    #     return True
