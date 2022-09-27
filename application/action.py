from abc import abstractmethod

from application.handler import Handler


class Action(Handler):

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return self._next_handler

    def get_next_action(self):
        return self._next_handler

    @abstractmethod
    def execute(row, col, direction, current_player, board):
        pass
