from constans.constants_scores import CORRECT_MOVE
from application.action import Action
from application.utils import target_position_within_bounds
from exceptions.personal_exceptions import invalidMoveException
from game.board import Board
from game.cell import Cell
from game.character import Character
from game.player import Player


class MoveToHole(Action):

    def execute(self, from_row, from_col, direction, current_player: Player, board: Board):
        to_row, to_col = target_position_within_bounds(from_row, from_col, direction)
        origin_cell: Cell = board.get_cell(from_row, from_col)
        target_cell: Cell = board.get_cell(to_row, to_col)
        character_origin_cell: Character = origin_cell.character

        # check if in the target cell has a hole
        if target_cell.has_hole:
            character_origin_cell.transfer_tresaure(origin_cell)
            origin_cell.remove_character()
            board.discover_cell(to_row, to_col, current_player)
            return CORRECT_MOVE

        # continue the chain of responsability
        elif self.get_next_action():
            return self.get_next_action().execute(from_row, from_col, direction, current_player, board)

        raise invalidMoveException("Invalid move")
