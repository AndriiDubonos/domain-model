from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type, Any

from domain_model.domain_events import BaseDomainEvent, EventsCollector
from domain_model.typing import AggregateData


@dataclass(frozen=True, slots=True)
class BaseCommand:
    command_name = None


class BaseCommandContext:
    pass


class CommandHandler(ABC):
    def __init__(self):
        self._events_collector = None

    def handle(
        self,
        data: AggregateData,
        command: BaseCommand,
        events_collector: EventsCollector,
        context: BaseCommandContext | None,
    ) -> Any | None:
        self._events_collector = events_collector
        result = self._handle(data, command, context)
        self._events_collector = None
        return result

    @abstractmethod
    def _handle(
        self,
        data: AggregateData,
        command: BaseCommand,
        context: BaseCommandContext | None,
    ) -> Any | None:
        pass

    def _add_event(self, event: BaseDomainEvent):
        self._events_collector.add_event(event)


class CommandsStorage:
    def __init__(self, commands_handlers: dict[Type[BaseCommand], CommandHandler]):
        self._commands_handlers = commands_handlers

    def get(self, command: BaseCommand) -> CommandHandler:
        command_type = type(command)
        try:
            return self._commands_handlers[command_type]
        except KeyError:
            raise ValueError(f'Unknown command type: {command_type}')
