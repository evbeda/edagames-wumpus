from application.action import Action
from constants.constants import KILL
from application.utils import target_position_within_bounds
from exceptions.personal_exceptions import invalidMoveException
from game.board import Board
from game.cell import Cell
from game.character import Character
from game.player import Player


class ShootAndKill(Action):

    def execute(self, row, col, direction, current_player: Player, board: Board):
        target_row, target_col = target_position_within_bounds(row, col, direction)
        target_cell: Cell = board.get_cell(target_row, target_col)
        character_to_kill: Character = target_cell.character

        # check if there is an opponent character
        if (character_to_kill and
           character_to_kill.player.user_name != current_player.user_name):
            current_player.arrows -= 1
            character_to_kill.transfer_tresaure(target_cell)
            target_cell.remove_character()
            board.discover_cell(target_row, target_col, current_player)
            return KILL

        elif self.get_next_action():
            return self.get_next_action().execute(row, col, direction, current_player, board)

        raise invalidMoveException("No available shoots")
