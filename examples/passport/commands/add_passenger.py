from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from domain_model.commands import BaseCommand, CommandHandler, BaseCommandContext
from domain_model.object_id import ObjectID
from examples.passport.data import Flight, Passenger
from examples.passport.events.passenger_added import PassengerAddedEvent
from examples.passport.events.passengers_count_approach_capacity import PassengersCountApproachCapacityEvent


@dataclass(frozen=True, slots=True)
class AddPassengerCommand(BaseCommand):
    command_name = 'add_passenger'

    user_id: UUID


class AddPassengerCommandHandler(CommandHandler):
    def _handle(
        self,
        data: Flight,
        command: AddPassengerCommand,
        context: BaseCommandContext | None,
    ) -> Any | None:
        if data.is_full:
            raise ValueError('Flight is full')

        new_passenger = Passenger(id=ObjectID(None), user_id=command.user_id, registration_date=datetime.now())
        data.passengers.append(new_passenger)

        if (percentage_full := len(data.passengers) / data.capacity) > 0.9:
            self._add_event(
                PassengersCountApproachCapacityEvent(capacity=data.capacity, current_count=len(data.passengers),
                                                     percentage_full=percentage_full))

        self._add_event(PassengerAddedEvent(passenger_id=new_passenger.id.value))
