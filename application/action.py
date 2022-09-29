from abc import abstractmethod

from application.handler import Handler
from game.board import Board
from game.player import Player


class Action(Handler):

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return self._next_handler

    def get_next_action(self):
        return self._next_handler

    @abstractmethod
    def execute(row: int, col: int, direction: str, current_player: Player, board: Board):
        pass
