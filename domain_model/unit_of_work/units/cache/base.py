class BaseCacheUnit(BaseUnit):
    async def __aenter__(self):
        raise NotImplementedError

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    def get_cache(self):
        raise NotImplementedError
