from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BaseDomainEvent:
    pass


class EventsCollector:
    def __init__(self):
        self._events = []

    def get_events(self) -> list[BaseDomainEvent]:
        return self._events

    def add_event(self, event: BaseDomainEvent):
        self._events += (event,)

    def __aenter__(self):
        return self

    def __aexit__(self, exc_type, exc_value, traceback):
        pass
