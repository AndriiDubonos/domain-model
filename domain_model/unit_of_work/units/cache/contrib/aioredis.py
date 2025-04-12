from aioredis import Redis

from domain_model.unit_of_work.units.cache import BaseCacheUnit


class RedisCacheUnit(BaseCacheUnit):

    def __init__(self, redis: Redis):
        super().__init__()
        self._redis: Redis = redis
        self._connection = None

    async def __aenter__(self):
        self._connection = await self._context.enter_async_context(self._redis)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._context.aclose()

    def get_cache(self):
        return self._connection

