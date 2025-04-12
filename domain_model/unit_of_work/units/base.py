from contextlib import AsyncExitStack


class BaseUnit:
    def __init__(self):
        self._context = AsyncExitStack()

    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def handle_exception(self, exc_type, exc_val, exc_tb):
        pass
