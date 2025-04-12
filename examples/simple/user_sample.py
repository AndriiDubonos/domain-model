from domain_model.aggregate import Aggregate
from domain_model.commands import CommandsStorage
from domain_model.repository import BaseRepository


class UserAggregate(Aggregate):
    pass


class UserRepository(BaseRepository):
    pass


def main():
    UserAggregate(commands_storage=CommandsStorage(), data={})
