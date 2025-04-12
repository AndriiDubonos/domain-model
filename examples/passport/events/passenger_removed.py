from dataclasses import dataclass
from uuid import UUID

from domain_model.domain_events import BaseDomainEvent


@dataclass(frozen=True, slots=True)
class PassengerRemovedEvent(BaseDomainEvent):
    passenger_id: UUID
