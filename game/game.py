from constans.constants_game import LARGE
from constans.constans import (
    PLAYER_1,
    INITIAL_POSITION_PLAYER_1,
    INITIAL_POSITION_PLAYER_2
)
from game.cell import Cell
from game.character import Character
from game.player import Player


class WumpusGame():

    def __init__(self) -> None:
        self._board = [
            [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)
        ]
        self.player_1 = None
        self.player_2 = None

    def move_to_own_character_position(self, player_game, row_to, col_to):
        if self._board[row_to][col_to].character.player == player_game:
            raise Exception("Bad Move")

    def place_character_initial_pos(
        self,
        player: Player,
        character1: Character,
        character2: Character,
        character3: Character
    ) -> None:
        list_positions = INITIAL_POSITION_PLAYER_1 if (
            player.name == PLAYER_1
            ) else INITIAL_POSITION_PLAYER_2

        character_positions = {
            list_positions[0]: character1,
            list_positions[1]: character2,
            list_positions[2]: character3
        }

        for position, character in character_positions.items():
            self._board[position[0]][position[1]].character = character
