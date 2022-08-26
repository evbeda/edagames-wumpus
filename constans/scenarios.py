
from copy import deepcopy
from constans.constants_game import LARGE
from constans.constans import (
    PLAYER_1,
    PLAYER_2
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

BOARD_WITH_TWO_CHARACTERS_SAME_PLAYER = [
    [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]

BOARD_WITH_TWO_CHARACTERS_SAME_PLAYER[0][0].character = Player(PLAYER_1)
BOARD_WITH_TWO_CHARACTERS_SAME_PLAYER[0][1].character = Player(PLAYER_1)

DANGER_SIGNAL_SCENARIO = [
    [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
DANGER_SIGNAL_SCENARIO[4][4].has_hole = True


TESTED_CELL_1 = Cell(0, 0)

TESTED_CELL_2 = Cell(0, 0)
TESTED_CELL_2.is_discover_by_player_1 = True

TESTED_CELL_3 = Cell(0, 0)
TESTED_CELL_3.character = Character(Player(PLAYER_2))
TESTED_CELL_3.is_discover_by_player_1 = True

TESTED_CELL_4 = Cell(0, 0)
TESTED_CELL_4.character = Character(Player(PLAYER_2))
TESTED_CELL_4.is_discover_by_player_2 = True

TESTED_CELL_5 = Cell(0, 0)
TESTED_CELL_5.has_hole = True
TESTED_CELL_5.is_discover_by_player_2 = True

TESTED_CELL_6 = Cell(0, 0)
TESTED_CELL_6.arrow = 1
TESTED_CELL_6.is_discover_by_player_2 = True

TESTED_CELL_7 = Cell(0, 0)
TESTED_CELL_7.gold = 2
TESTED_CELL_7.is_discover_by_player_2 = True

TESTED_CELL_8 = Cell(0, 0)
TESTED_CELL_8.diamond = 1
TESTED_CELL_8.is_discover_by_player_1 = True

TESTED_CELL_9 = Cell(0, 0)
TESTED_CELL_9.gold = 1
TESTED_CELL_9.diamond = 1
TESTED_CELL_9.is_discover_by_player_1 = True

TESTED_CELL_10 = Cell(0, 0)
TESTED_CELL_10.arrow = 1

FILTER_MOVE_BOARD_H = [
    [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
FILTER_MOVE_BOARD_H[5][5].has_hole = True
player_1 = Player(PLAYER_1)
character_player_1 = Character(player_1)
character_player_1.golds = 5
character_player_1.diamonds = 1
FILTER_MOVE_BOARD_H[5][4].character = character_player_1

FIN_FILTER_MOVE_BOARD_H = [
    [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
FIN_FILTER_MOVE_BOARD_H[5][5].has_hole = True
FIN_FILTER_MOVE_BOARD_H[5][4].gold = 5
FIN_FILTER_MOVE_BOARD_H[5][4].diamond = 1

DICTIONARY_H = {"from_row": 5,
                "from_col": 4,
                "to_row": 5,
                "to_col": 5,
                "player": PLAYER_1}

FILTER_MOVE_SAME_P = [
    [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
player_1 = Player(PLAYER_1)
character_player_1 = Character(player_1)
character_player_1.golds = 5
character_player_1.diamonds = 1
FILTER_MOVE_SAME_P[5][5].character = character_player_1
FILTER_MOVE_SAME_P[5][4].character = character_player_1

DICTIONARY_SM = {"from_row": 5,
                 "from_col": 4,
                 "to_row": 5,
                 "to_col": 5,
                 "player": PLAYER_1}

FILTER_MOVE_BOARD_ENE = [
    [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
player_2 = Player(PLAYER_2)
character_player_2 = Character(player_2)
FILTER_MOVE_BOARD_ENE[5][5].character = character_player_2
player_1 = Player(PLAYER_1)
character_player_1 = Character(player_1)
character_player_1.golds = 5
character_player_1.diamonds = 5
FILTER_MOVE_BOARD_ENE[5][4].character = character_player_1

FIN_FILTER_MOVE_BOARD_ENE = deepcopy(FILTER_MOVE_BOARD_ENE)
FIN_FILTER_MOVE_BOARD_ENE[5][4].character = None
FIN_FILTER_MOVE_BOARD_ENE[5][4].gold = 5
FIN_FILTER_MOVE_BOARD_ENE[5][4].diamond = 1

DICTIONARY_ENE = {"from_row": 5,
                  "from_col": 4,
                  "to_row": 5,
                  "to_col": 5,
                  "player": PLAYER_1}

DICTIONARY_MAK_MOV = {"from_row": 5,
                      "from_col": 4,
                      "to_row": 5,
                      "to_col": 5,
                      "player": PLAYER_1}

MAKE_MOVE_BOARD = [
    [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
player_1 = Player(PLAYER_1)
player_1.arrows = 1
character_player_1 = Character(player_1)
character_player_1.golds = 2
character_player_1.diamonds = 0
MAKE_MOVE_BOARD[5][4].character = character_player_1
MAKE_MOVE_BOARD[5][5].arrow = 1
MAKE_MOVE_BOARD[5][5].gold = 1

DICTIONARY_MAK_MOV_P2 = {"from_row": 5,
                         "from_col": 4,
                         "to_row": 5,
                         "to_col": 5,
                         "player": PLAYER_2}

MAKE_MOVE_BOARD_P2 = [
    [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
player_2 = Player(PLAYER_2)
player_2.arrows = 3
character_player_2 = Character(player_2)
character_player_2.golds = 2
character_player_2.diamonds = 0
MAKE_MOVE_BOARD_P2[5][4].character = character_player_2
MAKE_MOVE_BOARD_P2[5][5].arrow = 0
MAKE_MOVE_BOARD_P2[5][5].gold = 3
MAKE_MOVE_BOARD_P2[5][5].diamond = 1

DICT_FILTER_MOVE_MK = {"from_row": 5,
                       "from_col": 4,
                       "to_row": 5,
                       "to_col": 5,
                       "player": PLAYER_2}

FILTER_MOVE_MAKE_MOVE = [
    [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
player_2 = Player(PLAYER_2)
player_2.arrows = 3
character_player_2 = Character(player_2)
character_player_2.golds = 2
character_player_2.diamonds = 0
FILTER_MOVE_MAKE_MOVE[5][4].character = character_player_2
FILTER_MOVE_MAKE_MOVE[5][5].arrow = 0
FILTER_MOVE_MAKE_MOVE[5][5].gold = 3
FILTER_MOVE_MAKE_MOVE[5][5].diamond = 1

FIN_FILTER_MOVE_MAKE_MOVE = [
    [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
player_2 = Player(PLAYER_2)
player_2.arrows = 3
character_player_2 = Character(player_2)
character_player_2.golds = 2
character_player_2.diamonds = 0
FILTER_MOVE_MAKE_MOVE[5][5].character = character_player_2

<<<<<<< HEAD

PARSE_CELL_SCENARIO = [
    [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]

CELL_1 = Cell(0, 0)
CELL_1.character = Character(Player(PLAYER_2))
CELL_1.is_discover_by_player_2 = True

CELL_2 = Cell(0, 16)
CELL_2.character = Character(Player(PLAYER_1))
CELL_2.is_discover_by_player_1 = True

CELL_3 = Cell(8, 0)
CELL_3.character = Character(Player(PLAYER_2))
CELL_3.is_discover_by_player_2 = True

CELL_4 = Cell(8, 1)
CELL_4.character = Character(Player(PLAYER_1))
CELL_4.is_discover_by_player_1 = True

CELL_5 = Cell(10, 10)
CELL_5.character = Character(Player(PLAYER_2))
CELL_5.is_discover_by_player_2 = True

CELL_6 = Cell(10, 11)
CELL_6.character = Character(Player(PLAYER_1))
CELL_6.is_discover_by_player_1 = True

CELL_7 = Cell(10, 12)
CELL_7.has_hole = True

CELL_8 = Cell(10, 9)
CELL_8.has_hole = True

CELL_9 = Cell(4, 4)
CELL_9.arrow = 1

CELL_10 = Cell(4, 5)
CELL_10.arrow = 1
CELL_10.diamond = 1

CELL_11 = Cell(4, 6)
CELL_11.arrow = 1
CELL_11.gold = 1

CELL_12 = Cell(4, 7)
CELL_12.has_hole = True
CELL_12.is_discover_by_player_1 = True

CELL_13 = Cell(4, 9)
CELL_13.arrow = 1
CELL_13.is_discover_by_player_2 = True

CELL_14 = Cell(14, 5)
CELL_14.arrow = 1
CELL_14.gold = 3
CELL_14.is_discover_by_player_2 = True

CELL_15 = Cell(14, 6)
CELL_15.arrow = 1
CELL_15.gold = 3
CELL_15.diamond = 1
CELL_15.is_discover_by_player_2 = True

CELL_16 = Cell(5, 8)
CELL_16.character = Character(Player(PLAYER_1))

CELL_17 = Cell(4, 8)
CELL_17.is_discover_by_player_2 = True


PARSE_CELL_SCENARIO[0][0] = CELL_1
PARSE_CELL_SCENARIO[0][16] = CELL_2
PARSE_CELL_SCENARIO[8][0] = CELL_3
PARSE_CELL_SCENARIO[8][1] = CELL_4
PARSE_CELL_SCENARIO[10][10] = CELL_5
PARSE_CELL_SCENARIO[10][11] = CELL_6
PARSE_CELL_SCENARIO[10][12] = CELL_7
PARSE_CELL_SCENARIO[10][9] = CELL_8
PARSE_CELL_SCENARIO[4][4] = CELL_9
PARSE_CELL_SCENARIO[4][5] = CELL_10
PARSE_CELL_SCENARIO[4][6] = CELL_11
PARSE_CELL_SCENARIO[4][7] = CELL_12
PARSE_CELL_SCENARIO[4][9] = CELL_13
PARSE_CELL_SCENARIO[14][5] = CELL_14
PARSE_CELL_SCENARIO[14][6] = CELL_15

PARSE_CELL_SCENARIO[5][8] = CELL_16
PARSE_CELL_SCENARIO[4][8] = CELL_17
=======
BOARD_FOR_MOVE_AND_MODIFY_SCORE = [
    [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)
]
player_1 = Player(PLAYER_1)
character_player_1 = Character(player_1)
BOARD_FOR_MOVE_AND_MODIFY_SCORE[5][5].gold = 2
BOARD_FOR_MOVE_AND_MODIFY_SCORE[5][5].diamond = 1
>>>>>>> 8877e98 (Now, scores changes when getting items)
