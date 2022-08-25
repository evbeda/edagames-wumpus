import random

from constans.constans import (
    PLAYER_1,
    INITIAL_POSITION_PLAYER_1,
    INITIAL_POSITION_PLAYER_2
)
from constans.constants_game import GOLD, GOLD_QUANTITY, LARGE, MIDDLE

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
        self.place_golds()

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

    def place_golds(self):
        fisrt_half = (0, MIDDLE-1)
        second_half = (MIDDLE + 1, LARGE - 1)

        for start, end in [fisrt_half, second_half]:
            for _ in range(GOLD_QUANTITY//2):
                self.place_item(start, end, GOLD)

    def place_item(self, start: int, end: int, item):

        while True:  # busca hasta encontrar una posicion libre
            row = random.randint(0, LARGE - 1)
            col = random.randint(start, end)
            if self._board[row][col].empty:
                if item == GOLD:
                    self._board[row][col].gold += 1
                break

    def initial_diamond_position(self):
        self._board[random.randint(0, LARGE - 1)][LARGE//2].diamond += 1

    def drop_items(self, row, col):
        golds_player = self._board[row][col].character.golds
        diamonds_player = self._board[row][col].character.diamonds
        self._board[row][col].character = None
        self._board[row][col].diamond = diamonds_player
        self._board[row][col].gold = golds_player
