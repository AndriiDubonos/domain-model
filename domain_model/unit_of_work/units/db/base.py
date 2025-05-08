from domain_model.unit_of_work.units.base import BaseUnit


class BaseDBUnit(BaseUnit):
    def get_db_session(self):
        raise NotImplementedError

    async def rollback(self):
        raise NotImplementedError

    async def handle_exception(self, exc_type, exc_val, exc_tb):
        await self.rollback()
