
from copy import deepcopy
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

# scenarios to test recursive
RECURSIVE = [[Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
RECURSIVE[0][1].gold += 1

CLOSED_GOLD_BOARD = [[Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
CLOSED_GOLD_BOARD[4][3].has_hole = True
CLOSED_GOLD_BOARD[4][5].has_hole = True
CLOSED_GOLD_BOARD[3][4].has_hole = True
CLOSED_GOLD_BOARD[5][4].has_hole = True
CLOSED_GOLD_BOARD[4][4].gold += 1

INITIAL_BIG_FAIL_BOARD = [
    [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
for row in range(LARGE):
    INITIAL_BIG_FAIL_BOARD[row][4].has_hole = True
INITIAL_BIG_FAIL_BOARD[7][7].gold += 1

RECURSIVE_SIDE = [
    [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
RECURSIVE_SIDE[1][LARGE - 1].has_hole = True
RECURSIVE_SIDE[2][LARGE - 2].has_hole = True
RECURSIVE_SIDE[3][LARGE - 1].has_hole = True
RECURSIVE_SIDE[2][LARGE - 1].gold += 1


RECURSIVE_SIDE_CORNER = [
    [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
RECURSIVE_SIDE_CORNER[15][0].has_hole = True
RECURSIVE_SIDE_CORNER[16][1].has_hole = True
RECURSIVE_SIDE_CORNER[16][0].gold += 1


WAY_GOLD_TWO_PLAYERS = [
    [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
WAY_GOLD_TWO_PLAYERS[15][0].has_hole = True
WAY_GOLD_TWO_PLAYERS[16][1].has_hole = True
WAY_GOLD_TWO_PLAYERS[7][7].gold += 1

BOARD_GOLD_ITEMS = [[Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
player_1 = Player(PLAYER_1)
character_player_1 = Character(player_1)
character_player_1.golds = 0
character_player_1.diamonds = 0
BOARD_GOLD_ITEMS[5][8].character = character_player_1
BOARD_GOLD_ITEMS[5][8].gold = 1

BOARD_DIAMOND_ITEMS = [[Cell(i, j) for j in range(LARGE)]
                       for i in range(LARGE)]
player_1 = Player(PLAYER_1)
character_player_1 = Character(player_1)
character_player_1.golds = 0
character_player_1.diamonds = 0
BOARD_DIAMOND_ITEMS[5][8].character = character_player_1
BOARD_DIAMOND_ITEMS[5][8].diamond = 1


FIND_GOLD_POS_1 = [
    [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
FIND_GOLD_POS_1[5][7].gold += 1
FIND_GOLD_POS_1[2][7].gold += 1
FIND_GOLD_POS_1[1][7].gold += 1
FIND_GOLD_POS_1[7][4].gold += 1
FIND_GOLD_POS_1[7][1].gold += 1
FIND_GOLD_POS_1[3][6].gold += 1
FIND_GOLD_POS_1[2][9].gold += 1
FIND_GOLD_POS_1[10][7].gold += 1
FIND_GOLD_POS_1[9][7].gold += 1


FIND_GOLD_POS_2 = [
    [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
FIND_GOLD_POS_2[4][2].gold += 1
FIND_GOLD_POS_2[2][5].gold += 1
FIND_GOLD_POS_2[3][7].gold += 1
FIND_GOLD_POS_2[7][4].gold += 1

FIND_GOLD_POS_3 = [
    [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
FIND_GOLD_POS_3[4][2].gold += 1

FIND_GOLD_POS_4 = [
    [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]

VALID_HOLE_SCENARIO = deepcopy(INITIAL_BIG_FAIL_BOARD)
VALID_HOLE_SCENARIO[7][4].has_hole = False
VALID_HOLE_SCENARIO[0][2].has_hole = True
VALID_HOLE_SCENARIO[1][2].has_hole = True
VALID_HOLE_SCENARIO[2][2].has_hole = True
VALID_HOLE_SCENARIO[2][1].has_hole = True
VALID_HOLE_SCENARIO[4][10].gold += 1
