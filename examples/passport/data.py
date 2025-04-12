from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain_model.object_id import ObjectID


@dataclass
class Passenger:
    id: ObjectID

    user_id: UUID
    registration_date: datetime


@dataclass
class Flight:
    id: ObjectID

    departure_date: datetime
    arrival_date: datetime

    aircraft_id: UUID | None
    capacity: int

    passengers: list[Passenger]

    @property
    def is_full(self) -> bool:
        return len(self.passengers) >= self.capacity

    def get_passenger(self, passenger_id: UUID) -> Passenger:
        for passenger in self.passengers:
            if passenger.id == passenger_id:
                return passenger
        raise ValueError(f"Passenger with id {passenger_id} not found.")
