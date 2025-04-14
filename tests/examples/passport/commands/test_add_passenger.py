from datetime import datetime
from unittest import IsolatedAsyncioTestCase
from uuid import UUID, uuid4

from domain_model.domain_events import BaseDomainEvent
from domain_model.tests.command_runner import PassportCommandRunner
from domain_model.unit_of_work.unit_of_work import UnitOfWork
from examples.passport.commands.add_passenger import AddPassengerCommand
from examples.passport.data import Flight
from examples.passport.events.passengers_count_approach_capacity import PassengersCountApproachCapacityEvent
from examples.passport.passport import get_flight_passport
from examples.utils import TestingUnitTypes, InMemoryJSONDBUnit


class _CustomError(Exception):
    pass


class AddPassengerCommandTestCase(IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self._in_memory_unit = self._create_in_memory_unit()

    async def _execute(self, flight_id: UUID, command: AddPassengerCommand) -> tuple[Flight, list[BaseDomainEvent]]:
        async with UnitOfWork(units={TestingUnitTypes.IN_MEMORY_DB: self._in_memory_unit}) as unit_of_work:
            command_runner = PassportCommandRunner(passport=get_flight_passport())
            return await command_runner.run_commands(
                root_id=flight_id,
                commands=[command],
                unit_of_work=unit_of_work,
            )

    def _prepare_command(self, user_id: UUID) -> AddPassengerCommand:
        return AddPassengerCommand(user_id=user_id)

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
        flight, events = await self._execute(flight_id=flight_id, command=self._prepare_command(user_id))

        self.assertEqual(len(flight.passengers), 1)
        self.assertEqual(flight.passengers[0].user_id, user_id)

    async def _test_reaching_capacity(self, capacity: int, passengers: int, expected_approaching_capacity_event: bool):
        flight_id = self._store_flight(capacity=capacity, passengers=[uuid4() for _ in range(passengers)])
        command = self._prepare_command(user_id=uuid4())
        _, events = await self._execute(flight_id=flight_id, command=command)
        self.assertEqual(PassengersCountApproachCapacityEvent(capacity=capacity, current_count=passengers+1, percentage_full=(passengers+1)/capacity) in events, expected_approaching_capacity_event)

    async def test_under_reaching_approaching_capacity(self):
        await self._test_reaching_capacity(capacity=100, passengers=89, expected_approaching_capacity_event=False)

    async def test_reaching_approaching_capacity(self):
        await self._test_reaching_capacity(capacity=100, passengers=90, expected_approaching_capacity_event=True)
