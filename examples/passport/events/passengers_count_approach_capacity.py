from dataclasses import dataclass

from domain_model.domain_events import BaseDomainEvent


@dataclass(frozen=True, slots=True)
class PassengersCountApproachCapacityEvent(BaseDomainEvent):
    """Event emitted when the number of passengers approaches the flight capacity."""
    capacity: int
    current_count: int
    percentage_full: float
