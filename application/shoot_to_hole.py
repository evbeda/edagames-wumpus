from application.action import Action
from application.utils import target_position_within_bounds
from constans.constants_scores import CORRECT_MOVE
from exceptions.personal_exceptions import invalidMoveException
from game.board import Board
from game.cell import Cell
from game.player import Player


class ShootToHole(Action):

    def execute(self, row, col, direction, current_player: Player, board: Board):
        target_row, target_col = target_position_within_bounds(row, col, direction)
        target_cell: Cell = board.get_cell(target_row, target_col)

        # check if there is a hole
        if (target_cell.has_hole):
            current_player.arrows -= 1
            board.discover_cell(target_row, target_col, current_player)
            return CORRECT_MOVE

        elif self.get_next_action():
            return self.get_next_action().execute(row, col, direction, current_player, board)

        raise invalidMoveException("No available shoots")
