from domain_model.unit_of_work.units.base import BaseUnit


class BaseDBUnit(BaseUnit):
    def get_db_session(self):
        raise NotImplementedError

    async def rollback(self):
        raise NotImplementedError
