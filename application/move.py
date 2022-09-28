from application.action import Action

from application.utils import (
    is_a_player_character,
    target_position_within_bounds,
    is_frendly_fire,
)

from exceptions.personal_exceptions import (
    notYourCharacterException,
    noPossibleMoveException,
    moveToYourOwnCharPositionException,
    invalidMoveException,

)
from game.board import Board
from game.player import Player


class Move(Action):

    def execute(self, from_row: int, from_col: int, direction: str, current_player: Player, board: Board):

        # check if the character is a current_player character
        if not is_a_player_character(from_row, from_col, current_player, board):
            raise notYourCharacterException()

        # check if the direction is out of bounds (out of board)
        coordinates = target_position_within_bounds(from_row, from_col, direction)
        if coordinates is False:
            raise noPossibleMoveException()

        # reutilize the friendly fire method for moving to a same player character
        if is_frendly_fire(from_row, from_col, direction, current_player, board):
            raise moveToYourOwnCharPositionException()

        else:
            # continue the chain of responsability
            if self.get_next_action():
                return self.get_next_action().execute(from_row, from_col, direction, current_player, board)

            raise invalidMoveException("Invalid move")
