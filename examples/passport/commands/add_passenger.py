from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from domain_model.commands import BaseCommand, CommandHandler, BaseCommandContext
from domain_model.object_id import ObjectID
from examples.passport.data import Flight, Passenger
from examples.passport.events.passenger_added import PassengerAddedEvent


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

        self._add_event(PassengerAddedEvent(passenger_id=new_passenger.id.value))
