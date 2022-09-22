from dataclasses import dataclass
import random
from constans.constans import (
    EAST,
    FORBIDDEN_HOLE_CELLS,
    INITIAL_POSITIONS,
    NORTH,
    SOUTH,
    WEST,
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
from constans.constants_scores import (
    ARROW_MISS,
    CORRECT_MOVE,
    KILL,
)
from exceptions.personal_exceptions import (
    friendlyFireException,
    moveToYourOwnCharPositionException,
    noArrowsAvailableException,
    noPossibleMoveException,
    notYourCharacterException,
    shootOutOfBoundsException,
)
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
        for row_next, col_next in possible_moves:
            if (
                (row_next, col_next) not in visited and
                not self._board[row_next][col_next].has_hole and
                self._can_find_gold(row_next, col_next,
                                    gold_position, visited)
            ):
                return True
        return False

    def shoot_arrow(
        self,
        row: int,
        col: int,
        direction: str,
        current_player: Player,
    ) -> str:
        """
        Takes a coordenate, a direction and a current player.
        Returns the string with the result of the actions.
        In case the shoot kills an enemy returns "KILL".
        In case the shoot miss an opponent character returns "ARROW_MISS".
        In case the shoot hit a hole returns "CORRECT_MOVE".
        In case of an invalid move, raises an "invalidMoveException".
        """
        self.there_are_arrows_available(current_player)

        target_row, target_col = self.target_position(row, col, direction)
        target_cell = self._board[target_row][target_col]

        self.is_not_frendly_fire(target_cell, current_player)

        if (target_cell.character is not None and
           target_cell.character.player.name != current_player.name):
            result = self.kill_opp(target_row, target_col, current_player)

        elif target_cell.has_hole:
            result = self.shoot_hole(target_row, target_col, current_player)

        elif target_cell.character is None:
            result = self.shoot_miss(target_row, target_col, current_player)

        return result

    def there_are_arrows_available(
        self,
        current_player: Player,
    ) -> None:
        if current_player.arrows < 1:
            raise noArrowsAvailableException()

    def is_not_frendly_fire(
        self,
        target_cell: Cell,
        current_player: Player,
    ) -> None:
        if (
            target_cell.character is not None and
            target_cell.character.player.name == current_player.name
        ):
            current_player.arrows -= 1
            raise friendlyFireException()

    def kill_opp(
        self,
        row: int,
        col: int,
        current_player: Player,
    ) -> str:
        current_player.arrows -= 1
        cell = self._board[row][col]
        character_to_kill = cell.character
        character_to_kill.transfer_tresaure(cell)
        cell.remove_character()
        self.discover_cell(row, col, current_player)
        return KILL

    def shoot_miss(
        self,
        row: int,
        col: int,
        current_player: Player,
    ) -> str:
        # self.discover_cell(row, col, current_player)
        current_player.arrows -= 1
        self._board[row][col].arrow += 1
        return ARROW_MISS

    def shoot_hole(
        self,
        row: int,
        col: int,
        current_player: Player,
    ) -> str:
        self.discover_cell(row, col, current_player)
        current_player.arrows -= 1
        return CORRECT_MOVE

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

    def target_position(
        self,
        row: int,
        col: int,
        direction: str,
    ) -> "tuple[int, int]":
        directions = {
            EAST: (0, 1),
            SOUTH: (1, 0),
            WEST: (0, -1),
            NORTH: (-1, 0)
        }
        target_row = row + directions[direction][0]
        target_col = col + directions[direction][1]
        if (target_row < 0 or target_row > LARGE - 1
           or target_col < 0 or target_col > LARGE - 1):
            raise shootOutOfBoundsException()
        return (target_row, target_col)

    def move_to_own_character_position(self, current_player, row_to, col_to):
        ch = self._board[row_to][col_to].character
        if ch and ch.player == current_player:
            raise moveToYourOwnCharPositionException()

    def is_a_player_character(self, row, col, current_player):
        character = self._board[row][col].character
        return character.player.name == current_player.name if character else False

    def is_valid_move(
        self,
        from_row,
        from_col,
        to_row,
        to_col,
        current_player: Player
    ):
        coordinates = (to_row, to_col)
        if not self.is_a_player_character(from_row, from_col, current_player):
            raise notYourCharacterException()
        if (coordinates not in posibles_positions(from_row, from_col)):
            raise noPossibleMoveException()
        self.move_to_own_character_position(current_player, to_row, to_col)
        dictionary = {
            "from_row": from_row,
            "from_col": from_col,
            "to_row": to_row,
            "to_col": to_col,
            "player": current_player,
        }
        return self.filter_move(dictionary)

    def make_move(self, dictionary):
        from_row = dictionary["from_row"]
        from_col = dictionary["from_col"]
        to_row = dictionary["to_row"]
        to_col = dictionary["to_col"]
        current_player = dictionary["player"]
        new_cell: Cell = self._board[to_row][to_col]
        old_cel = self._board[from_row][from_col]
        character: Character = self._board[from_row][from_col].character
        character.player.arrows += new_cell.arrow
        new_cell.transfer_tresaure(character)
        new_cell.arrow = 0
        new_cell.character = character
        old_cel.character = None
        self.discover_cell(to_row, to_col, current_player)
        return CORRECT_MOVE

    def filter_move(self, dictionary):
        cell_to = self._board[dictionary["to_row"]][dictionary["to_col"]]
        current_player = dictionary["player"]
        character_cel = cell_to.character

        if cell_to.has_hole or (character_cel and
                                character_cel.player.name != current_player):
            row, col = dictionary["from_row"], dictionary["from_col"]
            cell = self._board[row][col]
            char = cell.character
            self.discover_cell(dictionary["to_row"], dictionary["to_col"], current_player)
            char.transfer_tresaure(cell)
            cell.remove_character()

            return CORRECT_MOVE
        else:
            return self.make_move(dictionary)

    def item_quantity(self, item):
        gold_quantity = sum([1 for row in self._board for cell in row if cell.gold > 0])
        hole_quantity = sum([1 for row in self._board for cell in row if cell.has_hole])
        return hole_quantity if item == HOLE else gold_quantity
