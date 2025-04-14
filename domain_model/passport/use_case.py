from abc import abstractmethod
from typing import Any, Generator
from uuid import UUID

from domain_model.commands import BaseCommand
from domain_model.domain_events import BaseDomainEvent
from domain_model.events_handlers import DomainEventsHandler
from domain_model.passport.passport import Passport
from domain_model.typing import AggregateData
from domain_model.unit_of_work.unit_of_work import UnitOfWork
from domain_model.use_case import BaseUseCase, convert_error


class BasePassportUseCase(BaseUseCase):
    def __init__(self, passport: Passport, error_class: type[Exception]):
        super().__init__(error_class=error_class)
        self._passport = passport

    async def execute(self, unit_of_work: UnitOfWork, root_id: UUID, raw_data: Any) -> Any:
        validated_data = await self._parse_and_validate(raw_data=raw_data)
        commands = list(self._generate_commands(validated_data=validated_data))

        if not commands:
            raise ValueError('No commands generated.')

        repo = self._passport.get_repository(unit_of_work=unit_of_work)

        with convert_error(self._error_class):
            aggregate = await repo.get(root_id=root_id)

        with convert_error(self._error_class):
            aggregate.handle_commands(commands=commands)

        await repo.save(aggregate=aggregate)

        aggregate_data = aggregate.get_data()
        events = aggregate.get_domain_events()
        await self._handle_events(aggregate_data=aggregate_data, events=events, unit_of_work=unit_of_work)

        return self._prepare_result(aggregate_data=aggregate_data, events=events)

    async def _parse_and_validate(self, raw_data: Any) -> Any:
        parsed_data = await self._parse(raw_data=raw_data)
        validated_data = await self._validate(parsed_data=parsed_data)
        return validated_data

    async def _parse(self, raw_data: Any) -> Any:
        return raw_data

    async def _validate(self, parsed_data: Any) -> Any:
        return parsed_data

    @abstractmethod
    def _generate_commands(self, validated_data: Any) -> Generator[BaseCommand, None, None]:
        raise NotImplementedError

    async def _handle_events(self, aggregate_data: AggregateData, events: list[BaseDomainEvent], unit_of_work: UnitOfWork) -> None:
        events_handler = self._get_events_handler()
        await events_handler.handle(data=aggregate_data, events=events, unit_of_work=unit_of_work)

    def _get_events_handler(self) -> DomainEventsHandler:
        return self._passport.get_events_handler()

    def _prepare_result(self, aggregate_data: AggregateData, events: list[BaseDomainEvent]) -> Any:
        return None


class BaseCreateAggregatePassportUseCase(BaseUseCase):
    def __init__(self, passport: Passport, error_class: type[Exception]):
        super().__init__(error_class=error_class)
        self._passport = passport

    async def execute(self, unit_of_work: UnitOfWork, root_id: UUID, raw_data: Any) -> Any:
        validated_data = await self._parse_and_validate(raw_data=raw_data)
        commands = list(self._generate_commands(validated_data=validated_data))

        if not commands:
            raise ValueError('No commands generated.')

        repo = self._passport.get_repository(unit_of_work=unit_of_work)

        with convert_error(self._error_class):
            aggregate = await repo.create()

        with convert_error(self._error_class):
            aggregate.handle_commands(commands=commands)

        await repo.save(aggregate=aggregate)

        aggregate_data = aggregate.get_data()
        events = aggregate.get_domain_events()
        await self._handle_events(aggregate_data=aggregate_data, events=events, unit_of_work=unit_of_work)

        return self._prepare_result(aggregate_data=aggregate_data, events=events)

    async def _parse_and_validate(self, raw_data: Any) -> Any:
        parsed_data = await self._parse(raw_data=raw_data)
        validated_data = await self._validate(parsed_data=parsed_data)
        return validated_data

    async def _parse(self, raw_data: Any) -> Any:
        return raw_data

    async def _validate(self, parsed_data: Any) -> Any:
        return parsed_data

    @abstractmethod
    def _generate_commands(self, validated_data: Any) -> Generator[BaseCommand, None, None]:
        raise NotImplementedError

    async def _handle_events(self, aggregate_data: AggregateData, events: list[BaseDomainEvent], unit_of_work: UnitOfWork) -> None:
        events_handler = self._get_events_handler()
        await events_handler.handle(data=aggregate_data, events=events, unit_of_work=unit_of_work)

    def _get_events_handler(self) -> DomainEventsHandler:
        return self._passport.get_events_handler()

    def _prepare_result(self, aggregate_data: AggregateData, events: list[BaseDomainEvent]) -> Any:
        return None
