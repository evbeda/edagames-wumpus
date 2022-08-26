import random

from constans.constans import (
    PLAYER_1,
    INITIAL_POSITION_PLAYER_1,
    INITIAL_POSITION_PLAYER_2,
    PLAYER_2
)
from constans.constants_game import (
    DIAMOND,
    GOLD,
    GOLD_QUANTITY,
    HOLE,
    HOLE_QUANTITY,
    LARGE,
    MIDDLE
    )

from game.cell import Cell
from game.character import Character
from game.player import Player
from game.utils import posibles_positions


class WumpusGame():

    def __init__(self) -> None:
        self._board = [
            [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)
        ]
        self.player_1 = Player(PLAYER_1)
        self.player_2 = Player(PLAYER_2)
        self.beto_1 = Character(self.player_1)
        self.beto_2 = Character(self.player_1)
        self.beto_3 = Character(self.player_1)
        self.perri_1 = Character(self.player_2)
        self.perri_2 = Character(self.player_2)
        self.perri_3 = Character(self.player_2)
        self.place_items(GOLD, GOLD_QUANTITY)
        self.place_items(HOLE, HOLE_QUANTITY)
        self.place_character_initial_pos(
            self.player_1,
            self.beto_1,
            self.beto_2,
            self.beto_3
        )
        self.place_character_initial_pos(
            self.player_2,
            self.perri_1,
            self.perri_2,
            self.perri_3
        )

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

    def place_items(self, item, item_quantity):
        fisrt_half = (0, MIDDLE-1)
        second_half = (MIDDLE + 1, LARGE - 1)

        for start, end in [fisrt_half, second_half]:
            for _ in range(item_quantity//2):
                self.place_items_in_free_position(start, end, item)

    def place_items_in_free_position(self, start: int, end: int, item):

        while True:  # busca hasta encontrar una posicion libre
            row = random.randint(0, LARGE - 1)
            col = random.randint(start, end)
            if self._board[row][col].empty:
                if item == GOLD:
                    self._board[row][col].gold += 1
                elif item == HOLE:
                    self._board[row][col].has_hole += 1
                break

    def initial_diamond_position(self):
        self._board[random.randint(0, LARGE - 1)][LARGE//2].diamond += 1

    def drop_items(self, row, col):
        golds_player = self._board[row][col].character.golds
        diamonds_player = self._board[row][col].character.diamonds
        self._board[row][col].character = None
        self._board[row][col].diamond = diamonds_player
        self._board[row][col].gold = golds_player

    def _can_find_gold(self, row, col, gold_position, board, visited):
        visited.append((row, col,))

        if (row, col) == gold_position:
            return True
        possible_moves = posibles_positions(row, col)

        for row_next, col_next in possible_moves:

            if (
                (row_next, col_next) not in visited and
                not board[row_next][col_next].has_hole and
                self._can_find_gold(row_next, col_next,
                                    gold_position, board, visited)
            ):
                return True
        return False

    def find_teasure(self, row, col, teasure):
        if teasure == GOLD and self._board[row][col].gold > 0:
            self._board[row][col].character.golds += self._board[row][col].gold
            self._board[row][col].gold = 0
        elif teasure == DIAMOND and self._board[row][col].diamond > 0:
            self._board[row][col].character.diamonds +=\
                self._board[row][col].diamond
            self._board[row][col].diamond = 0

    def discover_cell(self, character: Character, row, col):
        cell = self._board[row][col]
        # if cell.character == character:
        if character.player.name == PLAYER_1:
            cell.is_discover_by_player_1 = True
        else:
            cell.is_discover_by_player_2 = True
