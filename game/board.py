from dataclasses import dataclass
import random
from constans.constans import (
    FORBIDDEN_HOLE_CELLS,
    INITIAL_POSITIONS,
)
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
from game.diamond import Diamond
from game.gold import Gold
from game.utils import posibles_positions
from constans.constans import PLAYER_1
from game.player import Player


@dataclass
class PlayerPosition:
    row: int
    col: int


class Board():
    def __init__(self) -> None:
        self._board = [
            [Cell(row, col) for col in range(LARGE)] for row in range(LARGE)
        ]
        self._free_cells = []
        self._free_cells_left_half = []
        self._free_cells_right_half = []
        self.initialize_free_cells()
        self.place_items(GOLD, GOLD_QUANTITY)
        self.place_items(HOLE, HOLE_QUANTITY)
        self.initial_diamond_position()

    def initialize_free_cells(self):
        for row in self._board:
            for cell in row:
                self.decide_and_append(cell)

    def decide_and_append(self, cell):
        if (cell.position[1] < LARGE//2):
            self._free_cells_left_half.append(cell.position)
        if (cell.position[1] > LARGE//2):
            self._free_cells_right_half.append(cell.position)

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

    def initial_diamond_position(self) -> None:
        '''
        #  DEBUG LINES for multiple diamnods bug,
        #  left here in case further debugging is needed
        print("initial_diamond called")
        for row in range(LARGE):
            for t in self._board[row][LARGE//2].treasures:
                if isinstance(t, Diamond):
                    print("Already one diamond in the map")
        '''
        (
            self._board[random.randint(0, LARGE - 1)][LARGE//2]
            .treasures.append(Diamond())
        )

    def place_items(self, item, item_quantity):
        first_half = (0, MIDDLE-1)
        second_half = (MIDDLE + 1, LARGE - 1)
        for start, end in [first_half, second_half]:
            for _ in range(item_quantity//2):
                self.place_items_in_free_position(start, end, item)

    def place_items_in_free_position(self, start: int, end: int, item):
        if (start == 0):
            availableCells = self._free_cells_left_half
        else:
            availableCells = self._free_cells_right_half
        self.search_position_and_place_item(availableCells, item)

    def search_position_and_place_item(self, availableCells, item):
        '''
        Searchs available position and attemps to place item, validating
        every cell in availableCells and placing the item is
        placement is valid, otherwise removes the cell from
        available cells is that cell turns out to be invalid for
        positioning.
        '''
        while True:  # searches until it finds an available position
            myCoord = random.choice(availableCells)
            row = myCoord[0]
            col = myCoord[1]
            self.attempt_remove_cell(availableCells, myCoord)
            if self._is_valid(row, col, item):
                if item == GOLD:
                    self._board[row][col].treasures.append(Gold())
                elif item == HOLE:
                    self._board[row][col].has_hole = True
                break

    def attempt_remove_cell(self, availableCells: list, coord):
        try:
            availableCells.remove(coord)
        except ValueError:
            pass

    def _is_valid(
        self,
        row: int,
        col: int,
        item: str
    ) -> bool:
        cell = self.get_cell(row, col)
        if item == GOLD:
            return (cell.position not in INITIAL_POSITIONS and cell.empty)
        if item == HOLE and cell.position not in FORBIDDEN_HOLE_CELLS and not cell.has_hole:
            return self._valid_hole(row, col)

    def get_cell(self, row: int, col: int) -> Cell:
        cell = self._board[row][col]
        return cell

    def _valid_hole(self, row: int, col: int) -> bool:
        cell = self.get_cell(row, col)
        cell.put_hole()
        golds = self._gold_positions()
        for row_player, col_player in INITIAL_POSITIONS:
            player_position = PlayerPosition(row_player, col_player)
            if not self._player_can_find_gold(player_position, golds):
                cell.remove_hole()
                return False
        return True

    def _gold_positions(self) -> 'list[tuple]':
        return [
            (row, col)
            for row in range(LARGE)
            for col in range(LARGE)
            if self._board[row][col].gold > 0
        ]

    def _player_can_find_gold(
        self,
        player_position: PlayerPosition,
        golds,
    ) -> bool:
        for gold_position in golds:
            if not self._can_find_gold(
                player_position.row,
                player_position.col,
                gold_position,
                visited=[],
            ):
                return False
        return True

    def _can_find_gold(self, row, col, gold_position, visited):
        visited.append((row, col,))
        if (row, col) == gold_position:
            return True
        possible_moves = posibles_positions(row, col)
        possible_moves = self.sort_possibles_position(possible_moves, *gold_position)
        for row_next, col_next in possible_moves:
            if (
                (row_next, col_next) not in visited and
                not self._board[row_next][col_next].has_hole and
                self._can_find_gold(row_next, col_next,
                                    gold_position, visited)
            ):
                return True
        return False

    def sort_possibles_position(self, positions, destination_row, destination_col) -> list:
        def sorted_key(position) -> int:
            row, col = position
            # Euclidean distance between two points √((d_row - row)²+(d_col -col)²)
            # The 0.1 it's to give advantage to pick col direction over row direction going from left to right
            return ((destination_row - (row + 0.1)) ** 2 + (destination_col - col) ** 2) ** (0.5)
        return sorted(positions, key=sorted_key)

    def discover_cell(
        self,
        row: int,
        col: int,
        current_player: Player,
    ) -> None:
        cell = self._board[row][col]
        if current_player.name == PLAYER_1:
            cell.is_discover[0] = True
        else:
            cell.is_discover[1] = True

    def item_quantity(self, item):
        item_quantity = 0
        for row in self._board:
            for cell in row:
                item_quantity += (cell.gold > 0 and item == GOLD) or (cell.has_hole and item == HOLE)
        return item_quantity

    def has_opponent_player(self, character: Character, current_player: Player) -> bool:
        return character.player.name != current_player.name if character else False
