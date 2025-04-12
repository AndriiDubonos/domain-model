from typing import TypeVar, Any

AggregateData = TypeVar('AggregateData')
AggregateRawData = TypeVar('AggregateRawData')
CommandResult = TypeVar('CommandResult', bound=Any | None)
