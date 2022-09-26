from domain.action import Action

from domain.utils import (
    is_a_player_character,
    is_frendly_fire,
    target_position_within_bounds,
    there_are_arrows_available
)
from exceptions.personal_exceptions import (
    friendlyFireException,
    invalidMoveException,
    noArrowsAvailableException,
    notYourCharacterException,
    shootOutOfBoundsException,
)


class ShootArrow(Action):

    def execute(self, row, col, direction, current_player, board):
        # check available arrows
        if not there_are_arrows_available(current_player):
            raise noArrowsAvailableException()

        # check if the direction is out of bounds
        if not target_position_within_bounds(row, col, direction):
            raise shootOutOfBoundsException()

        # check if is a own character
        if not is_a_player_character(row, col, current_player, board):
            raise notYourCharacterException()

        # check if in the direction there are not a own character
        if is_frendly_fire(row, col, direction, current_player, board,):
            current_player.arrows -= 1
            raise friendlyFireException()

        else:
            if self.get_next_action():
                return self.get_next_action().execute(row, col, direction, current_player, board)

            raise invalidMoveException("No available shoots")
