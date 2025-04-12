from typing import Generator

from domain_model.commands import BaseCommand
from domain_model.passport.use_case import BasePassportUseCase
from examples.passport.commands.add_passenger import AddPassengerCommand
from examples.passport.passport import get_flight_passport


class AddPassengerUseCase(BasePassportUseCase):
    def __init__(self, error_class: type[Exception]):
        super().__init__(passport=get_flight_passport(), error_class=error_class)

    def _generate_commands(self, validated_data: dict) -> Generator[BaseCommand, None, None]:
        yield AddPassengerCommand(user_id=validated_data['user_id'])
