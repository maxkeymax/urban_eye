from typing import Any, List, Optional
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.future import select

from urban_eye.db.database import AsyncSession
from urban_eye.models.camera import Camera
from urban_eye.models.video import Video


class CameraCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_id(self, camera_uuid: UUID) -> Optional[Camera]:
        result = await self.db_session.execute(
            select(Camera).where(Camera.id == camera_uuid)
        )
        return result.scalars().first()

    async def create_camera(
        self,
        camera_id: str,
        camera_class_cd: int,
        camera_class: str,
        camera_name: str,
        camera_type_cd: int,
        camera_type: str,
        model: Optional[str] = None,
        camera_place: Optional[str] = None,
        camera_place_cd: Optional[int] = None,
        serial_number: Optional[str] = None,
        camera_latitude: Optional[float] = None,
        camera_longitude: Optional[float] = None,
        archive: bool = False,
        azimuth: Optional[int] = None,
    ) -> Camera:
        new_camera = Camera(
            camera_id=camera_id,
            camera_class_cd=camera_class_cd,
            camera_class=camera_class,
            camera_name=camera_name,
            camera_type_cd=camera_type_cd,
            camera_type=camera_type,
            model=model,
            camera_place=camera_place,
            camera_place_cd=camera_place_cd,
            serial_number=serial_number,
            camera_latitude=camera_latitude,
            camera_longitude=camera_longitude,
            archive=archive,
            azimuth=azimuth,
        )
        self.db_session.add(new_camera)
        await self.db_session.commit()
        await self.db_session.refresh(new_camera)
        return new_camera

    async def update_camera(
        self, camera_id: int, update_data: dict[str, Any]
    ) -> Optional[Camera]:
        camera = await self.get_by_id(camera_id)
        if not camera:
            return None

        for key, value in update_data.items():
            setattr(camera, key, value)

        await self.db_session.commit()
        await self.db_session.refresh(camera)
        return camera

    async def delete_camera(self, camera_id: int) -> bool:
        camera = await self.get_by_id(camera_id)
        if not camera:
            return False
        await self.db_session.delete(camera)
        await self.db_session.commit()
        return True

    async def get_all_as_geojson(self) -> dict[str, Any]:
        result = await self.db_session.execute(
            select(
                Camera.camera_id,
                Camera.camera_longitude,
                Camera.camera_latitude,
                func.count(Video.id).label("video_count")
            ).outerjoin(Camera.videos)
            .group_by(Camera.id)
        )
        features = []
        for camera in result.all():
            features.append({
                'type': 'Feature',
                'properties': {
                    'camera_id': camera.camera_id,
                    'has_video': camera.video_count > 0
                },
                'geometry': {
                    'type': 'Point',
                    'coordinates': [
                        camera.camera_longitude,
                        camera.camera_latitude
                    ]
                }
            })
        return {
            'type': 'FeatureCollection',
            'features': features
        }
        