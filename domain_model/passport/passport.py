from __future__ import annotations
from typing import Callable, Type

from domain_model.aggregate import Aggregate
from domain_model.commands import CommandsStorage
from domain_model.events_handlers import DomainEventsHandler
from domain_model.passport.repository import PassportRepository
from domain_model.repository import BaseRepository, BaseStorage
from domain_model.typing import AggregateData
from domain_model.unit_of_work.unit_of_work import UnitOfWork


def _get_default_repository_factory(storage_class: Type[BaseStorage]) -> Callable[[Passport, UnitOfWork], PassportRepository]:
    def _factory(passport: Passport, unit_of_work: UnitOfWork) -> PassportRepository:
        return PassportRepository(passport=passport, storage=storage_class(unit_of_work=unit_of_work))
    return _factory


def _default_aggregate_factory(data: AggregateData, commands_storage: CommandsStorage) -> Aggregate:
    return Aggregate(commands_storage=commands_storage, data=data)


class Passport:
    def __init__(
        self,
        commands_storage: CommandsStorage,
        repository_factory: Callable[[Passport, UnitOfWork], BaseRepository] = None,
        storage_class: Type[BaseStorage] = None,
        aggregate_factory: Callable[[AggregateData, CommandsStorage], Aggregate] = None,
        events_handler: DomainEventsHandler = None,
    ):
        self._commands_storage = commands_storage

        self._aggregate_factory = aggregate_factory or _default_aggregate_factory
        self._events_handler = events_handler or DomainEventsHandler({})

        if all((repository_factory, storage_class)) or not any((repository_factory, storage_class)):
            raise ValueError('Either `repository_factory` or `storage_class` must be provided, but not both.')

        self._repository_factory = repository_factory or _get_default_repository_factory(storage_class=storage_class)
        self._repository: BaseRepository | None = None

    def get_repository(self, unit_of_work: UnitOfWork) -> BaseRepository:
        if self._repository is None:
            self._repository = self._repository_factory(self, unit_of_work)

        return self._repository

    def create_aggregate(self, data: AggregateData) -> Aggregate:
        return self._aggregate_factory(data, self._commands_storage)

    def get_events_handler(self) -> DomainEventsHandler:
        return self._events_handler
