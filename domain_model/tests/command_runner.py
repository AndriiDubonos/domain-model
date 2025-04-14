from uuid import UUID

from domain_model.aggregate import Aggregate
from domain_model.commands import BaseCommand
from domain_model.domain_events import BaseDomainEvent
from domain_model.passport.passport import Passport
from domain_model.typing import AggregateData
from domain_model.unit_of_work.unit_of_work import UnitOfWork


class PassportCommandRunner:
    def __init__(self, passport: Passport):
        self._passport = passport

    async def run_commands(
        self,
        root_id: UUID,
        commands: list[BaseCommand],
        unit_of_work: UnitOfWork,
    ) -> tuple[AggregateData, list[BaseDomainEvent]]:
        repo = self._passport.get_repository(unit_of_work=unit_of_work)
        aggregate: Aggregate = await repo.get(root_id=root_id)
        aggregate.handle_commands(commands=commands)
        return aggregate.get_data(), aggregate.get_domain_events()
