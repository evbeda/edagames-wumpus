from constans.constants_game import LARGE
from game.cell import Cell


class WumpusGame():

    def __init__(self) -> None:
        self._board = [[Cell() for j in range(LARGE)] for i in range(LARGE)]
        self.player_1 = None
        self.player_2 = None

    def move_to_own_character_position(self, player_game, row_to, col_to):
        if self._board[row_to][col_to].character.player == player_game:
            raise Exception("Bad Move")
