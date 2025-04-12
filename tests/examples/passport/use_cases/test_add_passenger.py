from datetime import datetime
from unittest import IsolatedAsyncioTestCase
from uuid import UUID, uuid4

from domain_model.unit_of_work.unit_of_work import UnitOfWork
from examples.passport.use_cases.add_passenger import AddPassengerUseCase
from examples.utils import TestingUnitTypes, InMemoryJSONDBUnit


class AddPassengerUseCaseTestCase(IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self._in_memory_unit = self._create_in_memory_unit()

    async def _execute(self, flight_id: UUID, user_id: UUID = None):
        user_id = user_id or uuid4()
        use_case = AddPassengerUseCase(error_class=Exception)

        async with UnitOfWork(units={TestingUnitTypes.IN_MEMORY_DB: self._in_memory_unit}) as unit_of_work:
            await use_case.execute(
                unit_of_work=unit_of_work,
                root_id=flight_id,
                raw_data={'user_id': user_id},
            )

    def _create_in_memory_unit(self) -> InMemoryJSONDBUnit:
        return InMemoryJSONDBUnit()

    def _store_flight(self, capacity: int = 0) -> UUID:
        flight_id = uuid4()
        flight_data = {
            'id': str(flight_id),
            'departure_date': datetime.now(),
            'arrival_date': datetime.now(),
            'aircraft_id': None,
            'capacity': capacity,
            'passengers': [],
        }
        self._in_memory_unit.set(flight_id, flight_data)
        return flight_id

    async def test_execute(self):
        flight_id = self._store_flight(capacity=1)
        await self._execute(flight_id=flight_id)
