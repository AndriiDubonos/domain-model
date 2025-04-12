from dataclasses import dataclass
from typing import Any
from uuid import UUID

from domain_model.commands import BaseCommand, CommandHandler, BaseCommandContext
from examples.passport.data import Flight


@dataclass(frozen=True, slots=True)
class AssignAircraftCommand(BaseCommand):
    command_name = 'assign_aircraft'

    aircraft_id: UUID
    capacity: int


class AssignAircraftCommandHandler(CommandHandler):
    def _handle(
        self,
        data: Flight,
        command: AssignAircraftCommand,
        context: BaseCommandContext | None,
    ) -> Any | None:
        if data.aircraft_id is not None:
            raise ValueError('Flight already has an aircraft assigned')

        if command.capacity < len(data.passengers):
            raise ValueError('Aircraft capacity is less than the number of passengers')

        data.aircraft_id = command.aircraft_id
