import json
from typing import Any, Optional

import redis.asyncio as redis


class RedisCache:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def get_geojson(self, key: str) -> Optional[bytes]:
        cached = await self.redis.get(key)
        if cached:
            print('Данные из кеша')
            return json.loads(cached.decode("utf-8"))
        return None

    async def set_geojson(self, key: str, value: Any, ttl: int = 3) -> bool:
        print('Запись данных в кеш')
        return await self.redis.set(key, json.dumps(value), ex=ttl)
