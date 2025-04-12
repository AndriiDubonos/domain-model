from abc import ABC, abstractmethod
from uuid import UUID

from domain_model.aggregate import Aggregate
from domain_model.typing import AggregateData, AggregateRawData
from domain_model.unit_of_work.unit_of_work import UnitOfWork


class NotFoundError(Exception):
    def __init__(self, msg: str):
        msg = msg or 'Not found.'
        super().__init__(msg)
        self.message = msg


class BaseStorage(ABC):
    def __init__(self, unit_of_work: UnitOfWork):
        self._unit_of_work = unit_of_work

    @abstractmethod
    async def fetch_raw_data(self, root_id: UUID) -> AggregateRawData:
        pass

    @abstractmethod
    async def save(self, data: AggregateData) -> None:
        pass

    @abstractmethod
    def convert_raw_to_aggregate_data(self, raw_data: AggregateRawData) -> AggregateData:
        pass

    @abstractmethod
    async def initialize_new_raw_data(self) -> AggregateRawData:
        pass


class BaseRepository(ABC):
    def __init__(self, storage: BaseStorage):
        self._storage = storage

    async def create(self) -> Aggregate:
        raw_data = await self._storage.initialize_new_raw_data()
        aggregate_data = self._storage.convert_raw_to_aggregate_data(raw_data=raw_data)
        return self._init_aggregate(data=aggregate_data)

    async def get(self, root_id: UUID) -> Aggregate:
        raw_data = await self._storage.fetch_raw_data(root_id=root_id)
        aggregate_data = self._storage.convert_raw_to_aggregate_data(raw_data=raw_data)
        return self._init_aggregate(data=aggregate_data)

    async def save(self, aggregate: Aggregate) -> None:
        aggregate_data = aggregate.get_data()
        await self._storage.save(data=aggregate_data)

    @abstractmethod
    def _init_aggregate(self, data: AggregateData) -> Aggregate:
        raise NotImplementedError()
