from __future__ import annotations
from typing import Callable

from domain_model.aggregate import Aggregate
from domain_model.commands import CommandsStorage
from domain_model.events_handlers import DomainEventsHandler
from domain_model.repository import BaseRepository
from domain_model.typing import AggregateData
from domain_model.unit_of_work.unit_of_work import UnitOfWork


class Passport:
    def __init__(
        self,
        aggregate_factory: Callable[[AggregateData, CommandsStorage], Aggregate],
        commands_storage: CommandsStorage,
        repository_factory: Callable[[Passport, UnitOfWork], BaseRepository],
        events_handler: DomainEventsHandler,
    ):
        self._aggregate_factory = aggregate_factory
        self._commands_storage = commands_storage
        self._repository_factory = repository_factory
        self._events_handler = events_handler

        self._repository: BaseRepository | None = None

    def get_repository(self, unit_of_work: UnitOfWork) -> BaseRepository:
        if self._repository is None:
            self._repository = self._repository_factory(self, unit_of_work)

        return self._repository

    def create_aggregate(self, data: AggregateData) -> Aggregate:
        return self._aggregate_factory(data, self._commands_storage)

    def get_events_handler(self) -> DomainEventsHandler:
        return self._events_handler
