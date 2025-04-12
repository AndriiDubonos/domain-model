from abc import ABC, abstractmethod

from domain_model.domain_events import BaseDomainEvent
from domain_model.typing import AggregateData


class BaseEventHandler(ABC):
    @abstractmethod
    def handle(self, data: AggregateData, event: BaseDomainEvent) -> None:
        pass


class DomainEventsHandler(ABC):
    def __init__(self, subscribers: dict[type[BaseDomainEvent], tuple[BaseEventHandler, ...]]):
        self._subscribers = subscribers

    def handle(self, data: AggregateData, events: list[BaseDomainEvent]) -> None:
        for event in events:
            event_handlers = self._subscribers.get(type(event), tuple())
            if not event_handlers:
                continue
            for event_handler in event_handlers:
                event_handler.handle(data=data, event=event)
