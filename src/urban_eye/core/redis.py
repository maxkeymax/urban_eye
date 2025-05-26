import redis.asyncio as redis

from urban_eye.services.caching.redis_service import RedisCache
from urban_eye.settings import settings


async def get_redis_client():
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        decode_responses=False
    )
    return RedisCache(redis_client)
