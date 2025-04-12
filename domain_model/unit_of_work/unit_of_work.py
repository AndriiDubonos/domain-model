from contextlib import AsyncExitStack

from domain_model.unit_of_work.enums import UnitStatus
from domain_model.unit_of_work.typing import UnitTypeBase

from domain_model.unit_of_work.units.base import BaseUnit


class UnitOfWork:
    def __init__(
        self,
        units: dict[UnitTypeBase, BaseUnit],
    ):
        self._units = units
        self._status: UnitStatus = UnitStatus.READY

        self._units_statuses = {
            unit_type: UnitStatus.READY
            for unit_type, unit in self._units.items()
        }
        self._stack = AsyncExitStack()

    async def __aenter__(self):
        if self._status is not UnitStatus.READY:
            raise Exception('UnitOfWork could be entered only once.')

        self._status = UnitStatus.ENTERED
        # Units are lazy loaded when they are requested.

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            for unit_type, unit in self._units.items():
                if self._units_statuses[unit_type] is UnitStatus.ENTERED:
                    await unit.handle_exception(exc_type, exc_val, exc_tb)

        await self._stack.aclose()

        self._status = UnitStatus.EXITED
        self._units_statuses = {
            unit_type: UnitStatus.EXITED
            for unit_type, unit in self._units.items()
        }

    async def get_unit(self, unit_type: UnitTypeBase) -> BaseUnit:
        if self._status is not UnitStatus.ENTERED:
            raise Exception('UnitOfWork is not entered.')

        if unit_type not in self._units:
            raise Exception(f'Unit type {unit_type} is not supported.')

        await self._enter_unit(unit_type)

        return self._units[unit_type]

    async def _enter_unit(self, unit_type: UnitTypeBase):
        if self._units_statuses[unit_type] is UnitStatus.ENTERED:
            return

        if self._units_statuses[unit_type] is UnitStatus.EXITED:
            raise Exception('Unit is already exited.')

        await self._stack.enter_async_context(self._units[unit_type])

        self._units_statuses[unit_type] = UnitStatus.ENTERED
