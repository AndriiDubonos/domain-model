from abc import ABC, abstractmethod
from contextlib import  contextmanager
from typing import Any


@contextmanager
def convert_error(error_class: type[Exception]):
    try:
        yield
    except Exception as e:
        raise error_class from e


class BaseUseCase(ABC):
    def __init__(self, error_class: type[Exception]):
        self._error_class = error_class

    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        pass
