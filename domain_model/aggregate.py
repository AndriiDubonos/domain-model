from typing import Any

from domain_model.commands import BaseCommand, CommandsStorage, CommandHandler, BaseCommandContext
from domain_model.domain_events import BaseDomainEvent, EventsCollector
from domain_model.typing import AggregateData


class Aggregate:
    def __init__(self, commands_storage: CommandsStorage, data: AggregateData, events_collector: EventsCollector = None):
        self._data = data
        self._commands_storage = commands_storage
        self._events_collector: EventsCollector = events_collector or EventsCollector()

    def handle_commands(self, commands: list[BaseCommand]) -> dict[BaseCommand, Any | None]:
        context = self._before_commands(commands=commands)
        result = {}

        for command in commands:
            command_result = self._handle_command(command=command, context=context)
            result[command] =command_result
            self._log(command=command)

        self._after_commands(commands=commands, context=context)
        return result

    def get_data(self) -> AggregateData:
        return self._data

    def get_domain_events(self) -> list[BaseDomainEvent]:
        return self._events_collector.get_events()

    def _before_commands(self, commands: list[BaseCommand]) -> BaseCommandContext | None:
        pass

    def _after_commands(self, commands: list[BaseCommand], context: BaseCommandContext | None) -> None:
        pass

    def _handle_command(self, command: BaseCommand, context: BaseCommandContext) -> Any | None:
        handler = self._pick_handler(command=command)
        return handler.handle(
            data=self._data,
            command=command,
            context=context,
            events_collector=self._events_collector,
        )

    def _pick_handler(self, command: BaseCommand) -> CommandHandler:
        return self._commands_storage.get(command=command)

    def _log(self, command: BaseCommand) -> None:
        pass
