from enum import Enum
from uuid import UUID

from domain_model.unit_of_work.units.base import BaseUnit


class TestingUnitTypes(Enum):
    IN_MEMORY_DB = 'in_memory_db'


class InMemoryJSONDBUnit(BaseUnit):
    def __init__(self):
        super().__init__()
        self._storage = {}

    def get(self, key: UUID) -> dict:
        return self._storage[str(key)]

    def set(self, key: UUID, value: dict):
        self._storage[str(key)] = value
        return True

    async def handle_exception(self, exc_type, exc_val, exc_tb):
        pass
