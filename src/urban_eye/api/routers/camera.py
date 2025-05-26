from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from urban_eye.core.security import get_current_user
from urban_eye.db.database import get_db
from urban_eye.models.user import User
from urban_eye.repository.camera import CameraCRUD
from urban_eye.schemas.camera import (
    CameraCreate,
    CameraResponse,
    CameraUpdate,
    FeatureCollection,
)
from urban_eye.core.redis import get_redis_client
from urban_eye.services.caching.redis_service import RedisCache

router = APIRouter(prefix="/cameras", tags=["Cameras"])


@router.post("/", response_model=CameraResponse)
async def create_camera(
    camera_data: CameraCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CameraResponse:
    crud = CameraCRUD(db)
    try:
        return await crud.create_camera(**camera_data.model_dump())
    except IntegrityError as e:
        raise HTTPException(
            status_code=400,
            detail="Камера с таким ID уже существует"
            if "camera_id" in str(e)
            else "Ошибка при создании камеры",
        )


@router.get("/geojson", response_model=FeatureCollection)
async def get_cameras_geojson(
    name: Optional[str] = Query(None, description='Фильтр по названию камеры'),
    camera_type: Optional[str] = Query(None, description='Фильтр по типу камеры'),
    has_video: Optional[bool] = Query(None, description='Фильтр по наличию видео'),
    db: AsyncSession = Depends(get_db),
    redis_cache: RedisCache = Depends(get_redis_client),
    current_user: User = Depends(get_current_user)
) -> FeatureCollection:
    cache_key = f'geojson:{name}:{camera_type}:{has_video}'
    
    # Попробуем получить данные из	cache
    cached = await redis_cache.get_geojson(cache_key)
    if cached:
        return cached
    
    # Если данные не найдены, получаем их из базы данных
    crud = CameraCRUD(db)
    print('Данные из БД')
    geojson_data = await crud.get_all_as_geojson(
        name_filter=name,
        type_filter=camera_type,
        has_video_filter=has_video
    )
    
    # Сохраняем данные в кеш
    await redis_cache.set_geojson(cache_key, geojson_data)
    
    return geojson_data


@router.get("/{camera_id}", response_model=CameraResponse)
async def get_camera(
    camera_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CameraResponse:
    crud = CameraCRUD(db)
    camera = await crud.get_by_id(camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail="Камера не найдена")
    return camera


@router.put("/{camera_id}", response_model=CameraResponse)
async def update_camera(
    camera_id: UUID,
    update_data: CameraUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CameraResponse:
    crud = CameraCRUD(db)
    updated = await crud.update_camera(
        camera_id=camera_id, update_data=update_data.model_dump(exclude_unset=True)
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Камера не найдена")
    return updated


@router.delete("/{camera_id}")
async def delete_camera(
    camera_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    crud = CameraCRUD(db)
    deleted = await crud.delete_camera(camera_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Камера не найдена")
    return {"detail": "Камера успешно удалена"}
