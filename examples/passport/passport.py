from domain_model.aggregate import Aggregate
from domain_model.commands import CommandsStorage
from domain_model.events_handlers import DomainEventsHandler
from domain_model.passport.passport import Passport
from domain_model.passport.repository import PassportRepository
from examples.passport.storage import InMemoryFlightStorage
from examples.passport.commands.add_passenger import AddPassengerCommand, AddPassengerCommandHandler
from examples.passport.commands.remove_passenger import RemovePassengerCommand, RemovePassengerCommandHandler
from examples.passport.commands.assign_aircraft import AssignAircraftCommand, AssignAircraftCommandHandler
from examples.passport.events.passenger_added import PassengerAddedEvent
from examples.passport.events.passenger_removed import PassengerRemovedEvent


def get_flight_passport() -> Passport:
    return Passport(
        aggregate_factory=lambda data, commands_storage: Aggregate(commands_storage=commands_storage, data=data),
        commands_storage=CommandsStorage({
            AddPassengerCommand: AddPassengerCommandHandler(),
            RemovePassengerCommand: RemovePassengerCommandHandler(),
            AssignAircraftCommand: AssignAircraftCommandHandler(),
        }),
        repository_factory=lambda passport, unit_of_work: PassportRepository(
            passport=passport,
            storage=InMemoryFlightStorage(unit_of_work=unit_of_work),
        ),
        events_handler=DomainEventsHandler({}),
    )
