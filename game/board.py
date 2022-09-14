from constans.constans import FORBIDDEN_HOLE_CELLS, INITIAL_POSITIONS
from constans.constants_game import (
    GOLD,
    GOLD_QUANTITY,
    HOLE,
    HOLE_QUANTITY,
    LARGE,
    MIDDLE,
)
from game.cell import Cell
from game.character import Character
from game.gold import Gold
from game.utils import posibles_positions
import random


class Board():
    def __init__(self) -> None:
        self._board = [
            [Cell(row, col) for col in range(LARGE)] for row in range(LARGE)
        ]
        self.place_items(GOLD, GOLD_QUANTITY)
        self.place_items(HOLE, HOLE_QUANTITY)

    def place_character_initial_pos(
        self,
        characters: 'list[Character]',
        coordinates: 'list[tuple]',
        player_discover: int,
    ) -> None:
        for index, character in enumerate(characters):
            row, col = coordinates[index]
            self._board[row][col].character = character
            self._board[row][col].is_discover[player_discover] = True

    def place_items(self, item, item_quantity):
        fisrt_half = (0, MIDDLE-1)
        second_half = (MIDDLE + 1, LARGE - 1)
        for start, end in [fisrt_half, second_half]:
            for _ in range(item_quantity//2):
                self.place_items_in_free_position(start, end, item)

    def place_items_in_free_position(self, start: int, end: int, item):
        while True:  # search until find an available position
            row = random.randint(0, LARGE - 1)
            col = random.randint(start, end)
            if self._is_valid(row, col, item):
                if item == GOLD:
                    self._board[row][col].treasures.append(Gold())
                elif item == HOLE:
                    self._board[row][col].has_hole = True
                break

    def _is_valid(self, row, col, item) -> bool:
        valid = (
            (row, col) not in INITIAL_POSITIONS and
            self._board[row][col].empty)
        if item == HOLE and valid:
            valid = self._valid_hole(row, col)
        return valid

    def _valid_hole(self, row: int, col: int) -> bool:
        if (row, col) not in FORBIDDEN_HOLE_CELLS:
            self._board[row][col].has_hole = True
            golds = self._gold_positions()
            for row_player, col_player in INITIAL_POSITIONS:
                return self._player_can_find_gold(
                    row_player, col_player,
                    golds)
        else:
            return False

    def _gold_positions(self) -> 'list[tuple]':
        return [
            (row, col)
            for row in range(LARGE)
            for col in range(LARGE)
            if self._board[row][col].gold > 0
        ]

    def _player_can_find_gold(self, row, col, golds):
        for gold_position in golds:
            if not self._can_find_gold(row, col, gold_position, []):
                self._board[row][col].has_hole = False
                return False
        return True

    def _can_find_gold(self, row, col, gold_position, visited):
        visited.append((row, col,))
        if (row, col) == gold_position:
            return True
        possible_moves = posibles_positions(row, col)
        for row_next, col_next in possible_moves:
            if (
                (row_next, col_next) not in visited and
                not self._board[row_next][col_next].has_hole and
                self._can_find_gold(row_next, col_next,
                                    gold_position, visited)
            ):
                return True
        return False
