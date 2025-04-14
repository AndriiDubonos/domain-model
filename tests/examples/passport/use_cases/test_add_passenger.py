from datetime import datetime
from unittest import IsolatedAsyncioTestCase
from uuid import UUID, uuid4

from domain_model.unit_of_work.unit_of_work import UnitOfWork
from examples.passport.use_cases.add_passenger import AddPassengerUseCase
from examples.utils import TestingUnitTypes, InMemoryJSONDBUnit


class _CustomError(Exception):
    pass


class AddPassengerUseCaseTestCase(IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self._in_memory_unit = self._create_in_memory_unit()

    async def _execute(self, flight_id: UUID, user_id: UUID = None):
        user_id = user_id or uuid4()
        use_case = AddPassengerUseCase(error_class=_CustomError)

        async with UnitOfWork(units={TestingUnitTypes.IN_MEMORY_DB: self._in_memory_unit}) as unit_of_work:
            await use_case.execute(
                unit_of_work=unit_of_work,
                root_id=flight_id,
                raw_data={'user_id': user_id},
            )

    def _create_in_memory_unit(self) -> InMemoryJSONDBUnit:
        return InMemoryJSONDBUnit()

    def _store_flight(self, capacity: int = 0, passengers: list[UUID] = None) -> UUID:
        flight_id = uuid4()
        flight_data = {
            'id': str(flight_id),
            'departure_date': datetime.now(),
            'arrival_date': datetime.now(),
            'aircraft_id': None,
            'capacity': capacity,
            'passengers': [{
                'id': str(uuid4()),
                'user_id': str(user_id),
                'registration_date': datetime.now(),
            } for user_id in passengers] if passengers else [],
        }
        self._in_memory_unit.set(flight_id, flight_data)
        return flight_id

    async def test_add_passenger_to_empty_flight(self):
        user_id = uuid4()
        flight_id = self._store_flight(capacity=1)
        await self._execute(flight_id=flight_id, user_id=user_id)

        flight = self._in_memory_unit.get(flight_id)
        self.assertEqual(len(flight['passengers']), 1)
        self.assertEqual(flight['passengers'][0]['user_id'], str(user_id))

    async def test_add_passenger_to_flight(self):
        user_id = uuid4()
        flight_id = self._store_flight(capacity=2, passengers=[uuid4()])
        await self._execute(flight_id=flight_id, user_id=user_id)

        flight = self._in_memory_unit.get(flight_id)
        self.assertEqual(len(flight['passengers']), 2)
        self.assertEqual(flight['passengers'][1]['user_id'], str(user_id))

    async def _test_capacity(self, capacity: int, already_present_passengers: int):
        user_id = uuid4()
        flight_id = self._store_flight(capacity=capacity, passengers=[uuid4()] * already_present_passengers)
        await self._execute(flight_id=flight_id, user_id=user_id)

        flight = self._in_memory_unit.get(flight_id)
        self.assertEqual(len(flight['passengers']), already_present_passengers + 1)
        self.assertEqual(flight['passengers'][-1]['user_id'], str(user_id))

    async def test_add_passenger_under_capacity(self):
        await self._test_capacity(capacity=3, already_present_passengers=1)

    async def test_add_passenger_at_capacity(self):
        await self._test_capacity(capacity=3, already_present_passengers=2)

    async def test_add_passenger_over_capacity(self):
        with self.assertRaisesRegex(_CustomError, 'Flight is full'):
            await self._test_capacity(capacity=2, already_present_passengers=2)
