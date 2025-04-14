from domain_model.commands import CommandsStorage
from domain_model.events_handlers import DomainEventsHandler
from domain_model.passport.passport import Passport
from examples.passport.storage import InMemoryFlightStorage
from examples.passport.commands.add_passenger import AddPassengerCommand, AddPassengerCommandHandler
from examples.passport.commands.remove_passenger import RemovePassengerCommand, RemovePassengerCommandHandler
from examples.passport.commands.assign_aircraft import AssignAircraftCommand, AssignAircraftCommandHandler
from examples.passport.events.passenger_added import PassengerAddedEvent
from examples.passport.events.passenger_removed import PassengerRemovedEvent


def get_flight_passport() -> Passport:
    return Passport(
        commands_storage=CommandsStorage({
            AddPassengerCommand: AddPassengerCommandHandler(),
            RemovePassengerCommand: RemovePassengerCommandHandler(),
            AssignAircraftCommand: AssignAircraftCommandHandler(),
        }),
        storage_class=InMemoryFlightStorage,
        events_handler=DomainEventsHandler({}),
    )
