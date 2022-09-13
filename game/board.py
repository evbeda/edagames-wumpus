from constans.constants_game import LARGE
from game.cell import Cell
from game.character import Character


class Board():
    def __init__(self) -> None:
        self._board = [
            [Cell(row, col) for col in range(LARGE)] for row in range(LARGE)
        ]

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
