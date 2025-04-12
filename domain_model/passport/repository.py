from domain_model.aggregate import Aggregate
from domain_model.passport.passport import Passport
from domain_model.repository import BaseRepository, BaseStorage
from domain_model.typing import AggregateData


class PassportRepository(BaseRepository):
    def __init__(self, passport: Passport, storage: BaseStorage):
        super().__init__(storage=storage)
        self._passport = passport

    def _init_aggregate(self, data: AggregateData) -> Aggregate:
        return self._passport.create_aggregate(data=data)
