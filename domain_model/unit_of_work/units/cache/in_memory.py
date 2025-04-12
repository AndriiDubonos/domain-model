from domain_model.unit_of_work.units.cache.base import BaseCacheUnit


class InMemoryCacheUnit(BaseCacheUnit):
    def __init__(self):
        super().__init__()
        self._cache = InMemoryCache()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_cache(self):
        return self._cache


class InMemoryCache:
    def __init__(self):
        self.cache = {}

    async def get(self, key):
        return self.cache.get(key)

    async def set(self, key, value, ttl):
        self.cache[key] = value
        return True

    async def delete(self, key):
        if key in self.cache:
            del self.cache[key]
        return True
