from datetime import datetime
from typing import cast
from uuid import UUID

from domain_model.object_id import ObjectID
from domain_model.repository import BaseStorage
from examples.passport.data import Flight, Passenger
from examples.utils import TestingUnitTypes, InMemoryJSONDBUnit


class InMemoryFlightStorage(BaseStorage):
    async def fetch_raw_data(self, root_id: UUID) -> dict:
        in_memory_unit = await self._get_unit()
        return in_memory_unit.get(root_id)

    def convert_raw_to_aggregate_data(self, raw_data: dict) -> Flight:
        return Flight(
            id=ObjectID(raw_data['id']),
            departure_date=raw_data['departure_date'],
            arrival_date=raw_data['arrival_date'],
            aircraft_id=raw_data['aircraft_id'],
            capacity=raw_data['capacity'],
            passengers=[
                Passenger(
                    id=ObjectID(passenger['id']),
                    user_id=UUID(passenger['user_id']),
                    registration_date=passenger['registration_date'],
                )
                for passenger in raw_data['passengers']
            ],
        )

    async def initialize_new_raw_data(self) -> dict:
        return {
            'id': None,
            'departure_date': datetime.now(),
            'arrival_date': datetime.now(),
            'aircraft_id': None,
            'capacity': 0,
            'passengers': [],
        }

    async def save(self, data: Flight) -> None:
        in_memory_unit = await self._get_unit()
        in_memory_unit.set(
            data.id.value,
            {
                'id': str(data.id.value),
                'departure_date': data.departure_date,
                'arrival_date': data.arrival_date,
                'aircraft_id': str(data.aircraft_id) if data.aircraft_id else None,
                'capacity': data.capacity,
                'passengers': [
                    {
                        'id': str(passenger.id),
                        'user_id': str(passenger.user_id),
                        'registration_date': passenger.registration_date,
                    }
                    for passenger in data.passengers
                ],
            }
        )

    async def _get_unit(self) -> InMemoryJSONDBUnit:
        return cast(InMemoryJSONDBUnit, await self._unit_of_work.get_unit(TestingUnitTypes.IN_MEMORY_DB))
