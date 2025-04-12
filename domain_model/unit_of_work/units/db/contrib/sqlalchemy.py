from typing import Optional, Callable

from sqlalchemy.ext.asyncio import AsyncSession
from domain_model.unit_of_work.units.db.base import BaseDBUnit


class SQLAlchemySessionDBUnit(BaseDBUnit):
    def __init__(self, session_factory: Callable[[], AsyncSession] = None):
        super().__init__()
        self._session_factory = session_factory
        self._session: AsyncSession | None = None

    async def __aenter__(self):
        self._session = self._session_factory()
        await self._context.enter_async_context(self._session.begin())

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()

        await self._context.aclose()

    def get_db_session(self) -> AsyncSession:
        return self._session

    async def rollback(self):
        return await self._session.rollback()


class SQLAlchemyActiveTransactionSessionDBUnit(BaseDBUnit):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self._session: Optional[AsyncSession] = session

    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_db_session(self) -> AsyncSession:
        return self._session

    async def rollback(self):
        pass
