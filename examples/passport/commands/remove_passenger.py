from dataclasses import dataclass
from typing import Any
from uuid import UUID

from domain_model.commands import BaseCommand, CommandHandler, BaseCommandContext
from examples.passport.data import Flight
from examples.passport.events.passenger_removed import PassengerRemovedEvent


@dataclass(frozen=True, slots=True)
class RemovePassengerCommand(BaseCommand):
    command_name = 'remove_passenger'

    passenger_id: UUID


class RemovePassengerCommandHandler(CommandHandler):
    def _handle(
        self,
        data: Flight,
        command: RemovePassengerCommand,
        context: BaseCommandContext | None,
    ) -> Any | None:
        # Find and remove the passenger
        passenger = data.get_passenger(passenger_id=command.passenger_id)

        if passenger is None:
            raise ValueError(f'Passenger with id {command.passenger_id} not found')

        data.passengers.remove(passenger)

        # Add an event for the passenger removal
        self._add_event(PassengerRemovedEvent(passenger_id=command.passenger_id))
