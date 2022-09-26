from abc import ABC, abstractmethod


class Handler(ABC):
    """
    The Handler interface declares a method for building the chain of handlers.
    It also declares a method for executing a request.
    """

    def set_next(self, handler):
        pass

    @abstractmethod
    def execute():
        pass
