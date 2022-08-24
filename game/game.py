from constans.constants_game import LARGE
from game.cell import Cell
import random


class WumpusGame():

    def __init__(self) -> None:
        self._board = [[Cell() for j in range(LARGE)] for i in range(LARGE)]
        self.player_1 = None
        self.player_2 = None

    def initial_diamond_position(self):
        self._board[random.randint(0, LARGE - 1)][LARGE//2].diamond += 1
