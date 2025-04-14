from abc import ABC, abstractmethod

from domain_model.domain_events import BaseDomainEvent
from domain_model.typing import AggregateData
from domain_model.unit_of_work.unit_of_work import UnitOfWork


class BaseEventHandler(ABC):
    @abstractmethod
    async def handle(self, data: AggregateData, event: BaseDomainEvent, unit_of_work: UnitOfWork) -> None:
        pass


class DomainEventsHandler(ABC):
    def __init__(self, subscribers: dict[type[BaseDomainEvent], tuple[BaseEventHandler, ...]]):
        self._subscribers = subscribers

    async def handle(self, data: AggregateData, events: list[BaseDomainEvent], unit_of_work: UnitOfWork) -> None:
        for event in events:
            event_handlers = self._subscribers.get(type(event), tuple())
            if not event_handlers:
                continue
            for event_handler in event_handlers:
                await event_handler.handle(data=data, event=event, unit_of_work=unit_of_work)
