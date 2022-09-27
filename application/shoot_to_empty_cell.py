from application.action import Action
from constans.constants_scores import ARROW_MISS
from application.utils import target_position_within_bounds
from exceptions.personal_exceptions import invalidMoveException
from game.board import Board
from game.cell import Cell
from game.player import Player


class ShootEmptyCell(Action):

    def execute(self, row, col, direction, current_player: Player, board: Board):
        target_row, target_col = target_position_within_bounds(row, col, direction)
        target_cell: Cell = board.get_cell(target_row, target_col)

        # check if the cell does not have a character
        if (target_cell.character is None):
            current_player.arrows -= 1
            target_cell.arrow += 1
            return ARROW_MISS

        elif self.get_next_action():
            return self.get_next_action().execute(row, col, direction, current_player, board)

        raise invalidMoveException("No available shoots")
