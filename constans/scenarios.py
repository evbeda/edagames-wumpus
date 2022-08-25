
from constans.constants_game import LARGE
from constans.constans import (
    PLAYER_1
)
from game.cell import Cell
from game.character import Character
from game.player import Player

BOARD_WITH_ITEMS = [[Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
player_1 = Player(PLAYER_1)
character_player_1 = Character(player_1)
character_player_1.golds = 5
character_player_1.diamonds = 1
BOARD_WITH_ITEMS[5][5].character = character_player_1


BOARD_WIOUT_ITEMS = [[Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
player_1 = Player(PLAYER_1)
character_player_1 = Character(player_1)
character_player_1.golds = 0
character_player_1.diamonds = 0
BOARD_WIOUT_ITEMS[5][5].character = character_player_1
