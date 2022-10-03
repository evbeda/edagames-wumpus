from copy import deepcopy
from constants.constants import (
    HIDDEN_CELL,
    JOIN_ROW_BOARD,
    PLAYER_1,
    PLAYER_2,
    NAME_USER_1,
    NAME_USER_2,
    LARGE,
)
from game.cell import Cell
from game.character import Character
from game.player import Player
from game.diamond import Diamond
from game.gold import Gold

EMPTY_BOARD = [[Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]


def board_with_items():
    BOARD_WITH_ITEMS = deepcopy(EMPTY_BOARD)
    player_1 = Player(PLAYER_1, NAME_USER_1)
    character_player_1 = Character(player_1)
    character_player_1.treasures.append(Gold())
    character_player_1.treasures.append(Gold())
    character_player_1.treasures.append(Gold())
    character_player_1.treasures.append(Gold())
    character_player_1.treasures.append(Gold())
    character_player_1.treasures.append(Diamond())
    BOARD_WITH_ITEMS[5][5].character = character_player_1
    return (BOARD_WITH_ITEMS, player_1)


def board_without_items():
    BOARD_WIOUT_ITEMS = deepcopy(EMPTY_BOARD)
    player_1 = Player(PLAYER_1, NAME_USER_1)
    character_player_1 = Character(player_1)
    BOARD_WIOUT_ITEMS[5][5].character = character_player_1
    return (BOARD_WIOUT_ITEMS, player_1)


def empty_board():
    return EMPTY_BOARD


# scenarios to test recursive
def recursive():
    RECURSIVE = deepcopy(EMPTY_BOARD)
    RECURSIVE[0][1].treasures.append(Gold())
    return RECURSIVE


def closed_gold_board():
    CLOSED_GOLD_BOARD = deepcopy(EMPTY_BOARD)
    CLOSED_GOLD_BOARD[4][3].has_hole = True
    CLOSED_GOLD_BOARD[4][5].has_hole = True
    CLOSED_GOLD_BOARD[3][4].has_hole = True
    CLOSED_GOLD_BOARD[5][4].has_hole = True
    CLOSED_GOLD_BOARD[4][4].treasures.append(Gold())
    return CLOSED_GOLD_BOARD


def initial_big_fail_board():
    INITIAL_BIG_FAIL_BOARD = deepcopy(EMPTY_BOARD)
    for row in range(LARGE):
        INITIAL_BIG_FAIL_BOARD[row][4].has_hole = True
    INITIAL_BIG_FAIL_BOARD[7][7].treasures.append(Gold())
    return INITIAL_BIG_FAIL_BOARD


def recursive_side():
    RECURSIVE_SIDE = deepcopy(EMPTY_BOARD)
    RECURSIVE_SIDE[1][LARGE - 1].has_hole = True
    RECURSIVE_SIDE[2][LARGE - 2].has_hole = True
    RECURSIVE_SIDE[3][LARGE - 1].has_hole = True
    RECURSIVE_SIDE[2][LARGE - 1].treasures.append(Gold())
    return RECURSIVE_SIDE


def recursive_side_corner():
    RECURSIVE_SIDE_CORNER = deepcopy(EMPTY_BOARD)
    RECURSIVE_SIDE_CORNER[15][0].has_hole = True
    RECURSIVE_SIDE_CORNER[16][1].has_hole = True
    RECURSIVE_SIDE_CORNER[16][0].treasures.append(Gold())
    return RECURSIVE_SIDE_CORNER


def way_gold_two_players():
    WAY_GOLD_TWO_PLAYERS = deepcopy(EMPTY_BOARD)
    WAY_GOLD_TWO_PLAYERS[15][0].has_hole = True
    WAY_GOLD_TWO_PLAYERS[16][1].has_hole = True
    WAY_GOLD_TWO_PLAYERS[7][7].treasures.append(Gold())
    return WAY_GOLD_TWO_PLAYERS


def board_gold_items():
    BOARD_GOLD_ITEMS = deepcopy(EMPTY_BOARD)
    player_1 = Player(PLAYER_1, NAME_USER_1)
    character_player_1 = Character(player_1)
    BOARD_GOLD_ITEMS[5][8].character = character_player_1
    BOARD_GOLD_ITEMS[5][8].treasures.append(Gold())
    return BOARD_GOLD_ITEMS


def board_diamond_items():
    BOARD_DIAMOND_ITEMS = deepcopy(EMPTY_BOARD)
    player_1 = Player(PLAYER_1, NAME_USER_1)
    character_player_1 = Character(player_1)
    BOARD_DIAMOND_ITEMS[5][8].character = character_player_1
    BOARD_DIAMOND_ITEMS[5][8].treasures.append(Diamond())
    return BOARD_DIAMOND_ITEMS


def find_gold_pos_1():
    FIND_GOLD_POS_1 = deepcopy(EMPTY_BOARD)
    FIND_GOLD_POS_1[5][7].treasures.append(Gold())
    FIND_GOLD_POS_1[2][7].treasures.append(Gold())
    FIND_GOLD_POS_1[1][7].treasures.append(Gold())
    FIND_GOLD_POS_1[7][4].treasures.append(Gold())
    FIND_GOLD_POS_1[7][1].treasures.append(Gold())
    FIND_GOLD_POS_1[3][6].treasures.append(Gold())
    FIND_GOLD_POS_1[2][9].treasures.append(Gold())
    FIND_GOLD_POS_1[10][7].treasures.append(Gold())
    FIND_GOLD_POS_1[9][7].treasures.append(Gold())
    return FIND_GOLD_POS_1


def find_gold_pos_2():
    FIND_GOLD_POS_2 = deepcopy(EMPTY_BOARD)
    FIND_GOLD_POS_2[4][2].treasures.append(Gold())
    FIND_GOLD_POS_2[2][5].treasures.append(Gold())
    FIND_GOLD_POS_2[3][7].treasures.append(Gold())
    FIND_GOLD_POS_2[7][4].treasures.append(Gold())
    return FIND_GOLD_POS_2


def find_gold_pos_3():
    FIND_GOLD_POS_3 = deepcopy(EMPTY_BOARD)
    FIND_GOLD_POS_3[4][2].treasures.append(Gold())
    return FIND_GOLD_POS_3


def valid_hole_scenario():
    VALID_HOLE_SCENARIO = deepcopy(initial_big_fail_board())
    VALID_HOLE_SCENARIO[7][4].has_hole = False
    VALID_HOLE_SCENARIO[0][2].has_hole = True
    VALID_HOLE_SCENARIO[1][2].has_hole = True
    VALID_HOLE_SCENARIO[2][2].has_hole = True
    VALID_HOLE_SCENARIO[2][1].has_hole = True
    VALID_HOLE_SCENARIO[4][10].treasures.append(Gold())
    return VALID_HOLE_SCENARIO


def board_with_two_characters_same_player():
    BOARD_WITH_TWO_CHARACTERS_SAME_PLAYER = deepcopy(EMPTY_BOARD)

    BOARD_WITH_TWO_CHARACTERS_SAME_PLAYER[0][0].character = Player(PLAYER_1, NAME_USER_1)
    BOARD_WITH_TWO_CHARACTERS_SAME_PLAYER[0][1].character = Player(PLAYER_1, NAME_USER_1)
    return BOARD_WITH_TWO_CHARACTERS_SAME_PLAYER


def danger_signal_scenario():
    DANGER_SIGNAL_SCENARIO = deepcopy(EMPTY_BOARD)
    DANGER_SIGNAL_SCENARIO[4][4].has_hole = True
    return DANGER_SIGNAL_SCENARIO


def tested_cell():
    TESTED_CELL_1 = Cell(0, 0)
    TESTED_CELL_2 = Cell(0, 0)
    TESTED_CELL_2.is_discover[0] = True
    TESTED_CELL_3 = Cell(0, 0)
    TESTED_CELL_3.character = Character(Player(PLAYER_2, NAME_USER_2))
    TESTED_CELL_3.is_discover[0] = True
    TESTED_CELL_4 = Cell(0, 0)
    TESTED_CELL_4.character = Character(Player(PLAYER_2, NAME_USER_2))
    TESTED_CELL_4.is_discover[1] = True
    TESTED_CELL_5 = Cell(0, 0)
    TESTED_CELL_5.has_hole = True
    TESTED_CELL_5.is_discover[1] = True
    TESTED_CELL_6 = Cell(0, 0)
    TESTED_CELL_6.arrow = 1
    TESTED_CELL_6.is_discover[1] = True
    TESTED_CELL_7 = Cell(0, 0)
    TESTED_CELL_7.treasures.append(Gold())
    TESTED_CELL_7.treasures.append(Gold())
    TESTED_CELL_7.is_discover[1] = True
    TESTED_CELL_8 = Cell(0, 0)
    TESTED_CELL_8.treasures.append(Diamond())
    TESTED_CELL_8.is_discover[0] = True
    TESTED_CELL_9 = Cell(0, 0)
    TESTED_CELL_9.treasures.append(Gold())
    TESTED_CELL_9.treasures.append(Diamond())
    TESTED_CELL_9.is_discover[0] = True
    TESTED_CELL_10 = Cell(0, 0)
    TESTED_CELL_10.arrow = 1
    return [
        TESTED_CELL_1,
        TESTED_CELL_2,
        TESTED_CELL_3,
        TESTED_CELL_4,
        TESTED_CELL_5,
        TESTED_CELL_6,
        TESTED_CELL_7,
        TESTED_CELL_8,
        TESTED_CELL_9,
        TESTED_CELL_10,
    ]


def filter_move_board_h():
    FILTER_MOVE_BOARD_H = deepcopy(EMPTY_BOARD)
    FILTER_MOVE_BOARD_H[5][5].has_hole = True
    player_1 = Player(PLAYER_1, NAME_USER_1)
    character_player_1 = Character(player_1)
    player_1.characters = []
    player_1.characters.append(character_player_1)
    character_player_1.treasures.append(Gold())
    character_player_1.treasures.append(Gold())
    character_player_1.treasures.append(Gold())
    character_player_1.treasures.append(Gold())
    character_player_1.treasures.append(Gold())
    character_player_1.treasures.append(Diamond())
    FILTER_MOVE_BOARD_H[5][4].character = character_player_1
    return FILTER_MOVE_BOARD_H


def fin_filter_move_board_h():
    FIN_FILTER_MOVE_BOARD_H = deepcopy(EMPTY_BOARD)
    FIN_FILTER_MOVE_BOARD_H[5][5].has_hole = True
    FIN_FILTER_MOVE_BOARD_H[5][4].treasures.append(Gold())
    FIN_FILTER_MOVE_BOARD_H[5][4].treasures.append(Gold())
    FIN_FILTER_MOVE_BOARD_H[5][4].treasures.append(Gold())
    FIN_FILTER_MOVE_BOARD_H[5][4].treasures.append(Gold())
    FIN_FILTER_MOVE_BOARD_H[5][4].treasures.append(Gold())
    FIN_FILTER_MOVE_BOARD_H[5][4].treasures.append(Diamond())
    return FIN_FILTER_MOVE_BOARD_H


DICTIONARY_H = {"from_row": 5,
                "from_col": 4,
                "to_row": 5,
                "to_col": 5,
                "player": Player(PLAYER_1, NAME_USER_1)}


def filter_move_same_p():
    FILTER_MOVE_SAME_P = deepcopy(EMPTY_BOARD)
    player_1 = Player(PLAYER_1, NAME_USER_1)
    character_player_1 = Character(player_1)
    character_player_1.treasures.append(Gold())
    character_player_1.treasures.append(Gold())
    character_player_1.treasures.append(Gold())
    character_player_1.treasures.append(Gold())
    character_player_1.treasures.append(Gold())
    character_player_1.treasures.append(Diamond())
    FILTER_MOVE_SAME_P[5][5].character = character_player_1
    FILTER_MOVE_SAME_P[5][4].character = character_player_1
    return FILTER_MOVE_SAME_P


DICTIONARY_SM = {
    "from_row": 5,
    "from_col": 4,
    "to_row": 5,
    "to_col": 5,
    "player": PLAYER_1}


def filter_move_board_ene():
    FILTER_MOVE_BOARD_ENE = deepcopy(EMPTY_BOARD)
    player_2 = Player(PLAYER_2, NAME_USER_2)
    character_player_2 = Character(player_2)
    FILTER_MOVE_BOARD_ENE[5][5].character = character_player_2
    player_1 = Player(PLAYER_1, NAME_USER_1)
    character_player_1 = Character(player_1)
    player_1.characters = []
    player_1.characters.append(character_player_1)
    character_player_1.treasures.append(Gold())
    character_player_1.treasures.append(Gold())
    character_player_1.treasures.append(Gold())
    character_player_1.treasures.append(Gold())
    character_player_1.treasures.append(Gold())
    character_player_1.treasures.append(Diamond())
    character_player_1.treasures.append(Diamond())
    character_player_1.treasures.append(Diamond())
    character_player_1.treasures.append(Diamond())
    character_player_1.treasures.append(Diamond())
    FILTER_MOVE_BOARD_ENE[5][4].character = character_player_1

    FIN_FILTER_MOVE_BOARD_ENE = deepcopy(FILTER_MOVE_BOARD_ENE)
    FIN_FILTER_MOVE_BOARD_ENE[5][4].character = None
    FIN_FILTER_MOVE_BOARD_ENE[5][4].treasures.append(Gold())
    FIN_FILTER_MOVE_BOARD_ENE[5][4].treasures.append(Gold())
    FIN_FILTER_MOVE_BOARD_ENE[5][4].treasures.append(Gold())
    FIN_FILTER_MOVE_BOARD_ENE[5][4].treasures.append(Gold())
    FIN_FILTER_MOVE_BOARD_ENE[5][4].treasures.append(Gold())
    FIN_FILTER_MOVE_BOARD_ENE[5][4].treasures.append(Diamond())
    return FILTER_MOVE_BOARD_ENE


DICTIONARY_ENE = {
    "from_row": 5,
    "from_col": 4,
    "to_row": 5,
    "to_col": 5,
    "player": Player(PLAYER_1, NAME_USER_1)}

DICTIONARY_MAK_MOV = {
    "from_row": 5,
    "from_col": 4,
    "to_row": 5,
    "to_col": 5,
    "player": Player(PLAYER_1, NAME_USER_1)}


def make_move_board():
    MAKE_MOVE_BOARD = deepcopy(EMPTY_BOARD)
    player_1 = Player(PLAYER_1, NAME_USER_1)
    player_1.arrows = 1
    character_player_1 = Character(player_1)
    character_player_1.treasures = [Gold(), Gold()]
    MAKE_MOVE_BOARD[5][4].character = character_player_1
    MAKE_MOVE_BOARD[5][5].arrow = 1
    MAKE_MOVE_BOARD[5][5].treasures.append(Gold())
    return MAKE_MOVE_BOARD


DICTIONARY_MAK_MOV_P2 = {
    "from_row": 5,
    "from_col": 4,
    "to_row": 5,
    "to_col": 5,
    "player": Player(PLAYER_2, NAME_USER_2)}


def make_move_board_p2():
    MAKE_MOVE_BOARD_P2 = deepcopy(EMPTY_BOARD)
    player_2 = Player(PLAYER_2, NAME_USER_2)
    player_2.arrows = 3
    character_player_2 = Character(player_2)
    character_player_2.treasures.append(Gold())
    character_player_2.treasures.append(Gold())
    MAKE_MOVE_BOARD_P2[5][4].character = character_player_2
    MAKE_MOVE_BOARD_P2[5][5].arrow = 0
    MAKE_MOVE_BOARD_P2[5][5].treasures.append(Gold())
    MAKE_MOVE_BOARD_P2[5][5].treasures.append(Gold())
    MAKE_MOVE_BOARD_P2[5][5].treasures.append(Gold())
    MAKE_MOVE_BOARD_P2[5][5].treasures.append(Diamond())
    return MAKE_MOVE_BOARD_P2


DICT_FILTER_MOVE_MK = {
    "from_row": 5,
    "from_col": 4,
    "to_row": 5,
    "to_col": 5,
    "player": Player(PLAYER_2, NAME_USER_2)}


def filter_move_make_move():
    FILTER_MOVE_MAKE_MOVE = deepcopy(EMPTY_BOARD)
    player_2 = Player(PLAYER_2, NAME_USER_2)
    player_2.arrows = 3
    character_player_2 = Character(player_2)
    character_player_2.treasures.append(Gold())
    character_player_2.treasures.append(Gold())
    FILTER_MOVE_MAKE_MOVE[5][4].character = character_player_2
    FILTER_MOVE_MAKE_MOVE[5][5].arrow = 0
    FILTER_MOVE_MAKE_MOVE[5][5].treasures.append(Gold())
    FILTER_MOVE_MAKE_MOVE[5][5].treasures.append(Gold())
    FILTER_MOVE_MAKE_MOVE[5][5].treasures.append(Gold())
    FILTER_MOVE_MAKE_MOVE[5][5].treasures.append(Gold())
    FILTER_MOVE_MAKE_MOVE[5][5].treasures.append(Diamond())
    return FILTER_MOVE_MAKE_MOVE


def fin_filter_move_make_move():
    FIN_FILTER_MOVE_MAKE_MOVE = deepcopy(EMPTY_BOARD)
    player_2 = Player(PLAYER_2, NAME_USER_2)
    player_2.arrows = 3
    character_player_2 = Character(player_2)
    character_player_2.treasures.append(Gold())
    character_player_2.treasures.append(Gold())
    FIN_FILTER_MOVE_MAKE_MOVE[5][5].character = character_player_2
    return FIN_FILTER_MOVE_MAKE_MOVE


def parce_cell_scenario_instanciate_cell(
    row,
    col,
    player='',
    name_user='',
    discover_index=None,
    treasures=[],
    has_hole=False,
    arrow=0,
):
    cell = Cell(row, col)
    cell.is_discover[discover_index] = False if discover_index is None else True
    if not has_hole:
        cell.character = Character(Player(player, name_user))
        cell.treasures.extend([treasures])
    elif arrow != 0:
        cell.arrow = arrow
        cell.treasures.extend([treasures])
    elif has_hole:
        cell.has_hole = has_hole
    return cell


def parcel_cell_scenario_create_cells():
    CELL_1 = parce_cell_scenario_instanciate_cell(0, 0, PLAYER_2, NAME_USER_2, 1)
    CELL_2 = parce_cell_scenario_instanciate_cell(0, 16, PLAYER_1, NAME_USER_1, 0)
    CELL_3 = parce_cell_scenario_instanciate_cell(8, 0, PLAYER_2, NAME_USER_2, 1)
    CELL_4 = parce_cell_scenario_instanciate_cell(8, 1, PLAYER_1, NAME_USER_1, 0)
    CELL_5 = parce_cell_scenario_instanciate_cell(10, 10, PLAYER_2, NAME_USER_2, 1)
    CELL_6 = parce_cell_scenario_instanciate_cell(10, 11, PLAYER_1, NAME_USER_1, 0)
    CELL_7 = parce_cell_scenario_instanciate_cell(10, 12, has_hole=True)
    CELL_8 = parce_cell_scenario_instanciate_cell(10, 9, has_hole=True)
    CELL_9 = parce_cell_scenario_instanciate_cell(4, 4, arrow=1)
    CELL_10 = parce_cell_scenario_instanciate_cell(4, 5, arrow=1, treasures=[Diamond()])
    CELL_11 = parce_cell_scenario_instanciate_cell(4, 6, arrow=1, treasures=[Gold()])
    CELL_12 = parce_cell_scenario_instanciate_cell(4, 7, has_hole=True, discover_index=0)
    CELL_13 = parce_cell_scenario_instanciate_cell(4, 9, arrow=1, discover_index=1)
    CELL_14 = parce_cell_scenario_instanciate_cell(
        14, 5, arrow=1, treasures=[Gold(), Gold(), Gold()], discover_index=1)
    CELL_15 = parce_cell_scenario_instanciate_cell(
        14, 6, arrow=1,
        treasures=[Gold(), Gold(), Gold(), Diamond()], discover_index=1)
    CELL_16 = parce_cell_scenario_instanciate_cell(5, 8, PLAYER_1, NAME_USER_1)
    CELL_17 = parce_cell_scenario_instanciate_cell(4, 8, discover_index=1)
    return [
        CELL_1, CELL_2, CELL_3, CELL_4, CELL_5, CELL_6, CELL_7, CELL_8, CELL_9,
        CELL_10, CELL_11, CELL_12, CELL_13, CELL_14, CELL_15, CELL_16, CELL_17]


def parse_cell_scenario():
    PARSE_CELL_SCENARIO = deepcopy(EMPTY_BOARD)
    (
        PARSE_CELL_SCENARIO[0][0],
        PARSE_CELL_SCENARIO[0][16],
        PARSE_CELL_SCENARIO[8][0],
        PARSE_CELL_SCENARIO[8][1],
        PARSE_CELL_SCENARIO[10][10],
        PARSE_CELL_SCENARIO[10][11],
        PARSE_CELL_SCENARIO[10][12],
        PARSE_CELL_SCENARIO[10][9],
        PARSE_CELL_SCENARIO[4][4],
        PARSE_CELL_SCENARIO[4][5],
        PARSE_CELL_SCENARIO[4][6],
        PARSE_CELL_SCENARIO[4][7],
        PARSE_CELL_SCENARIO[4][9],
        PARSE_CELL_SCENARIO[14][5],
        PARSE_CELL_SCENARIO[14][6],
        PARSE_CELL_SCENARIO[5][8],
        PARSE_CELL_SCENARIO[4][8]
    ) = parcel_cell_scenario_create_cells()
    return PARSE_CELL_SCENARIO


def board_for_move_and_modify_score():
    BOARD_FOR_MOVE_AND_MODIFY_SCORE = deepcopy(EMPTY_BOARD)
    player_1 = Player(PLAYER_1, NAME_USER_1)
    character_player_1 = Character(player_1)
    BOARD_FOR_MOVE_AND_MODIFY_SCORE[5][5].treasures.append(Gold())
    BOARD_FOR_MOVE_AND_MODIFY_SCORE[5][5].treasures.append(Gold())
    BOARD_FOR_MOVE_AND_MODIFY_SCORE[5][5].treasures.append(Diamond())
    return (BOARD_FOR_MOVE_AND_MODIFY_SCORE, character_player_1)


def test_board_init_player_1():
    TEST_BOARD_INIT_PLAYER_1 = JOIN_ROW_BOARD.join([
        HIDDEN_CELL * LARGE
        if i != 0 and i != 8 and i != 16
        else
        '  B  ' + HIDDEN_CELL * 16
        for i in range(LARGE)
    ])
    return TEST_BOARD_INIT_PLAYER_1


def test_board_init_player_2():
    TEST_BOARD_INIT_PLAYER_2 = JOIN_ROW_BOARD.join([
        HIDDEN_CELL * LARGE
        if i != 0 and i != 8 and i != 16
        else
        HIDDEN_CELL * 16 + '  P  '
        for i in range(LARGE)
    ])
    return TEST_BOARD_INIT_PLAYER_2


PARSE_CELL_SCENARIO_STR_PLAYER_2 = (
    "  R  ################################################################################"
    "#####################################################################################"
    "#####################################################################################"
    "#####################################################################################"
    "######################F####F####F#######~   +  F  ###################################"
    "#####################################################################################"
    "#####################################################################################"
    "#####################################################################################"
    "  R +################################################################################"
    "#####################################################################################"
    "##################################################~ R +##############################"
    "#####################################################################################"
    "#####################################################################################"
    "#####################################################################################"
    "######################### 3F   3FD ##################################################"
    "#####################################################################################"
    "#####################################################################################"
)


PARSE_CELL_SCENARIO_STR_PLAYER_1 = (
    "################################################################################  L  "
    "#####################################################################################"
    "#####################################################################################"
    "#####################################################################################"
    "######################F####F####F##  O  #######F#####################################"
    "#####################################################################################"
    "#####################################################################################"
    "#####################################################################################"
    "#####  L +###########################################################################"
    "#####################################################################################"
    "#######################################################~ L +#########################"
    "#####################################################################################"
    "#####################################################################################"
    "#####################################################################################"
    "###########################F####F####################################################"
    "#####################################################################################"
    "#####################################################################################"
)


def board_with_only_characters():
    BOARD_WITH_ONLY_CHARACTERS = deepcopy(EMPTY_BOARD)
    pl_1 = Player(PLAYER_1, NAME_USER_1)
    pl_2 = Player(PLAYER_2, NAME_USER_2)
    BOARD_WITH_ONLY_CHARACTERS[0][0].character = pl_1.characters[0]
    BOARD_WITH_ONLY_CHARACTERS[8][0].character = pl_1.characters[1]
    BOARD_WITH_ONLY_CHARACTERS[16][0].character = pl_1.characters[2]
    BOARD_WITH_ONLY_CHARACTERS[0][16].character = pl_2.characters[0]
    BOARD_WITH_ONLY_CHARACTERS[8][16].character = pl_2.characters[0]
    BOARD_WITH_ONLY_CHARACTERS[16][16].character = pl_2.characters[0]
    return BOARD_WITH_ONLY_CHARACTERS


def board_player_1_scenario():
    scenario = deepcopy(board_with_only_characters())
    scenario[0][0].is_discover[0] = True
    scenario[8][0].is_discover[0] = True
    scenario[16][0].is_discover[0] = True
    return scenario


def scenario_str_player_1():
    return (
        "  L  ################################################################################"
        "#####################################################################################"
        "#####################################################################################"
        "#####################################################################################"
        "#####################################################################################"
        "#####################################################################################"
        "#####################################################################################"
        "#####################################################################################"
        "  L  ################################################################################"
        "#####################################################################################"
        "#####################################################################################"
        "#####################################################################################"
        "#####################################################################################"
        "#####################################################################################"
        "#####################################################################################"
        "#####################################################################################"
        "  L  ################################################################################"
    )


def test_players_character_0():
    TEST_PLAYERS_CHARACTER_0 = Player(PLAYER_1, NAME_USER_1)
    TEST_PLAYERS_CHARACTER_0.characters[0].treasures.extend([Gold()])
    TEST_PLAYERS_CHARACTER_0.characters[1].treasures.extend([Gold()])
    TEST_PLAYERS_CHARACTER_0.characters[2].treasures.extend([Diamond()])
    return TEST_PLAYERS_CHARACTER_0


def test_players_character_1():
    TEST_PLAYERS_CHARACTER_1 = Player(PLAYER_1, NAME_USER_1)
    TEST_PLAYERS_CHARACTER_1.characters[0].treasures.extend([Gold(), Gold(),
                                                            Gold(), Gold(),
                                                            Gold()])
    TEST_PLAYERS_CHARACTER_1.characters[1].treasures.extend([Diamond(), Gold()])
    TEST_PLAYERS_CHARACTER_1.characters[2].treasures.extend([Gold()])
    return TEST_PLAYERS_CHARACTER_1


def test_players_character_2():
    TEST_PLAYERS_CHARACTER_2 = Player(PLAYER_1, NAME_USER_1)
    TEST_PLAYERS_CHARACTER_2.score = 1000
    return TEST_PLAYERS_CHARACTER_2


# shoot scenarios
def scenarios_shoot_test():
    SCENARIOS_SHOOT_TEST = deepcopy(EMPTY_BOARD)
    CELL_SHOOT_8_8 = Cell(8, 8)
    SHOOTER_PLAYER = Player(PLAYER_1, NAME_USER_1)
    SHOOTED_PLAYER = Player(PLAYER_2, NAME_USER_2)
    CELL_SHOOT_8_8.character = SHOOTER_PLAYER.characters[0]
    CELL_SHOOT_8_8.is_discover[0] = True
    return (SCENARIOS_SHOOT_TEST, SHOOTED_PLAYER, SHOOTER_PLAYER)


def generate_board_for_shoot_action_test():
    scenario = deepcopy(EMPTY_BOARD)

    shooter_player = Player(PLAYER_1, NAME_USER_1)
    shotted_player = Player(PLAYER_2, NAME_USER_2)

    # add one more character to test cases
    shooter_player.characters.append(Character(shooter_player))
    shotted_player.characters.append(Character(shotted_player))

    (
        cell_shoot_8_8, cell_shoot_7_8, cell_shoot_9_8,
        cell_shoot_8_7, cell_shoot_4_4, cell_shoot_4_3,
        cell_shoot_4_5, cell_shoot_3_4, cell_shoot_5_4,
        cell_shoot_0_0, cell_shoot_0_1, cell_shoot_1_0,
        ) = cells_for_move_shoot_board(shooter_player, shotted_player)

    scenario[8][8] = cell_shoot_8_8
    scenario[7][8] = cell_shoot_7_8
    scenario[9][8] = cell_shoot_9_8
    scenario[8][7] = cell_shoot_8_7

    scenario[4][4] = cell_shoot_4_4
    scenario[4][3] = cell_shoot_4_3
    scenario[4][5] = cell_shoot_4_5
    scenario[3][4] = cell_shoot_3_4
    scenario[5][4] = cell_shoot_5_4

    scenario[0][0] = cell_shoot_0_0
    scenario[0][1] = cell_shoot_0_1
    scenario[1][0] = cell_shoot_1_0

    return scenario, shooter_player, shotted_player


def cells_for_move_shoot_board(shooter_player, shoted_player):

    # shooter cell 1
    cell_shoot_8_8 = Cell(8, 8)
    cell_shoot_8_8.character = shooter_player.characters[0]
    cell_shoot_8_8.is_discover[0] = True

    # cell with hole
    cell_shoot_7_8 = Cell(7, 8)
    cell_shoot_7_8.has_hole = True

    # cell with own chracter
    cell_shoot_9_8 = Cell(9, 8)
    cell_shoot_9_8.character = shooter_player.characters[0]
    cell_shoot_9_8.is_discover[0] = True

    # discovered cell with opponent character
    cell_shoot_8_7 = Cell(8, 7)
    cell_shoot_8_7.character = shoted_player.characters[0]
    cell_shoot_8_7.is_discover[0] = True

    # shooter cell 2
    cell_shoot_4_4 = Cell(4, 4)
    cell_shoot_4_4.character = shooter_player.characters[0]
    cell_shoot_4_4.is_discover[0] = True

    # covered cell with opponent character
    cell_shoot_4_3 = Cell(4, 3)
    cell_shoot_4_3.character = shoted_player.characters[1]
    cell_shoot_4_3.is_discover[0] = False

    # discovered empty cell
    cell_shoot_4_5 = Cell(4, 5)
    cell_shoot_4_5.is_discover[0] = True

    # covered opponent charact with treasures
    cell_shoot_3_4 = Cell(3, 4)
    cell_shoot_3_4.character: Character = shoted_player.characters[2]
    cell_shoot_3_4.character.treasures.extend([Gold(), Gold(), Diamond()])

    # a covered cell with treasures
    cell_shoot_5_4 = Cell(5, 4)
    cell_shoot_5_4.treasures.append(Gold())

    # shooter cell 3
    cell_shoot_0_0 = Cell(0, 0)
    cell_shoot_0_0.character = shooter_player.characters[3]
    cell_shoot_0_0.is_discover[0] = True

    # discovered opponent charact with treasures
    cell_shoot_0_1 = Cell(0, 1)
    cell_shoot_0_1.character: Character = shoted_player.characters[3]
    cell_shoot_0_1.character.treasures.extend([Gold(), Gold(), Gold()])
    cell_shoot_0_1.is_discover[0] = True

    # a discovered cell with treasures
    cell_shoot_1_0 = Cell(1, 0)
    cell_shoot_1_0.treasures.append(Gold())
    cell_shoot_1_0.is_discover[0] = True
    return [cell_shoot_8_8, cell_shoot_7_8, cell_shoot_9_8, cell_shoot_8_7,
            cell_shoot_4_4, cell_shoot_4_3, cell_shoot_4_5, cell_shoot_3_4, cell_shoot_5_4,
            cell_shoot_0_0, cell_shoot_0_1, cell_shoot_1_0, ]


def kill_opp_scenario():
    scenarios = deepcopy(EMPTY_BOARD)
    player_1 = Player(PLAYER_1, NAME_USER_1)
    player_2 = Player(PLAYER_2, NAME_USER_2)

    opp_character: Character = player_2.characters[0]
    opp_character.treasures.append(Diamond())
    opp_character.treasures.append(Gold())
    opp_character.treasures.append(Gold())

    scenarios[0][1].character = opp_character

    return scenarios, player_1, player_2


def shoot_n_kill_scenario():
    scenarios = deepcopy(EMPTY_BOARD)
    player_1 = Player(PLAYER_1, NAME_USER_1)
    player_2 = Player(PLAYER_2, NAME_USER_2)

    opp_character = player_2.characters[0]
    opp_character.treasures.append(Diamond())
    opp_character.treasures.append(Gold())
    opp_character.treasures.append(Gold())

    scenarios[0][1].character = opp_character

    return scenarios, player_1, player_2


def duplicate_first_coor_for_golds_placement():
    DUPLICATE_FIRST_COOR_FOR_GOLDS_PLACEMENT = [
        (2, 4), (2, 4), (4, 6), (5, 2), (7, 6), (9, 2), (11, 4), (11, 6), (12, 0),
        (4, 10), (4, 12), (4, 15), (9, 10), (10, 16), (11, 12), (13, 12), (14, 10),
    ]
    return DUPLICATE_FIRST_COOR_FOR_GOLDS_PLACEMENT


def duplicate_first_coor_for_holes_placement():
    DUPLICATE_FIRST_COOR_FOR_HOLES_PLACEMENT = [
        (3, 1), (3, 1), (3, 10), (3, 13), (4, 4), (6, 2), (6, 14), (8, 4), (9, 14),
        (12, 11), (12, 14), (13, 2), (13, 4), (15, 2), (15, 12), (15, 14), (16, 4),
    ]
    return DUPLICATE_FIRST_COOR_FOR_HOLES_PLACEMENT


def left_half_coords():
    return [
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
        (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7),
        (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7),
        (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7),
        (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7),
        (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7),
        (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7),
        (9, 0), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7),
        (10, 0), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7),
        (11, 0), (11, 1), (11, 2), (11, 3), (11, 4), (11, 5), (11, 6), (11, 7),
        (12, 0), (12, 1), (12, 2), (12, 3), (12, 4), (12, 5), (12, 6), (12, 7),
        (13, 0), (13, 1), (13, 2), (13, 3), (13, 4), (13, 5), (13, 6), (13, 7),
        (14, 0), (14, 1), (14, 2), (14, 3), (14, 4), (14, 5), (14, 6), (14, 7),
        (15, 0), (15, 1), (15, 2), (15, 3), (15, 4), (15, 5), (15, 6), (15, 7),
        (16, 0), (16, 1), (16, 2), (16, 3), (16, 4), (16, 5), (16, 6), (16, 7),
    ]


def right_half_coords():
    return [
        (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (0, 16),
        (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (1, 16),
        (2, 9), (2, 10), (2, 11), (2, 12), (2, 13), (2, 14), (2, 15), (2, 16),
        (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15), (3, 16),
        (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15), (4, 16),
        (5, 9), (5, 10), (5, 11), (5, 12), (5, 13), (5, 14), (5, 15), (5, 16),
        (6, 9), (6, 10), (6, 11), (6, 12), (6, 13), (6, 14), (6, 15), (6, 16),
        (7, 9), (7, 10), (7, 11), (7, 12), (7, 13), (7, 14), (7, 15), (7, 16),
        (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), (8, 14), (8, 15), (8, 16),
        (9, 9), (9, 10), (9, 11), (9, 12), (9, 13), (9, 14), (9, 15), (9, 16),
        (10, 9), (10, 10), (10, 11), (10, 12), (10, 13), (10, 14), (10, 15),
        (10, 16),
        (11, 9), (11, 10), (11, 11), (11, 12), (11, 13), (11, 14), (11, 15),
        (11, 16),
        (12, 9), (12, 10), (12, 11), (12, 12), (12, 13), (12, 14), (12, 15),
        (12, 16),
        (13, 9), (13, 10), (13, 11), (13, 12), (13, 13), (13, 14), (13, 15),
        (13, 16),
        (14, 9), (14, 10), (14, 11), (14, 12), (14, 13), (14, 14), (14, 15),
        (14, 16),
        (15, 9), (15, 10), (15, 11), (15, 12), (15, 13), (15, 14), (15, 15),
        (15, 16),
        (16, 9), (16, 10), (16, 11), (16, 12), (16, 13), (16, 14), (16, 15),
        (16, 16)
    ]


def generate_board_for_move_action_test():
    scenarios = deepcopy(EMPTY_BOARD)
    moving_player = Player(PLAYER_1, NAME_USER_1)
    opponent_player = Player(PLAYER_2, NAME_USER_2)
    # add one more character to test cases
    moving_player.characters.append(Character(moving_player))
    opponent_player.characters.append(Character(opponent_player))

    (
        cell_move_4_4, cell_move_4_3, cell_move_4_5,
        cell_move_3_4, cell_move_5_4, cell_move_8_8,
        cell_move_8_7, cell_move_8_9, cell_move_7_8,
        cell_move_9_8, cell_move_0_0) = cells_for_move_action_board(moving_player, opponent_player)

    scenarios[4][4] = cell_move_4_4
    scenarios[4][3] = cell_move_4_3
    scenarios[4][5] = cell_move_4_5
    scenarios[3][4] = cell_move_3_4
    scenarios[5][4] = cell_move_5_4
    scenarios[8][8] = cell_move_8_8
    scenarios[8][7] = cell_move_8_7
    scenarios[8][9] = cell_move_8_9
    scenarios[7][8] = cell_move_7_8
    scenarios[9][8] = cell_move_9_8
    scenarios[0][0] = cell_move_0_0
    return scenarios, moving_player, opponent_player


def cells_for_move_action_board(moving_player, opponent_player) -> list:

    # moving character 1
    cell_move_4_4 = Cell(4, 4)
    cell_move_4_4.character = moving_player.characters[0]
    cell_move_4_4.is_discover[0] = True

    # covered cell with hole
    cell_move_4_3 = Cell(4, 3)
    cell_move_4_3.has_hole = True

    # discovered cell empty
    cell_move_4_5 = Cell(4, 5)
    cell_move_4_5.is_discover[0] = True

    # discovered cell with opponent char
    cell_move_3_4 = Cell(3, 4)
    cell_move_3_4.character = opponent_player.characters[0]
    cell_move_3_4.is_discover[0] = True

    # discovered cell with own char
    cell_move_5_4 = Cell(5, 4)
    cell_move_5_4.character = moving_player.characters[1]
    cell_move_5_4.is_discover[0] = True

    # moving character 2 carrying treasures
    cell_move_8_8 = Cell(8, 8)
    cell_move_8_8.character: Character = moving_player.characters[2]
    cell_move_8_8.character.treasures.append(Gold())
    cell_move_8_8.is_discover[0] = True

    # discovered cell with hole
    cell_move_8_7 = Cell(8, 7)
    cell_move_8_7.has_hole = True
    cell_move_8_7.is_discover[0] = True

    # covered cell with treasures
    cell_move_8_9 = Cell(8, 9)
    cell_move_8_9.treasures.extend([Gold(), Gold(), Diamond()])
    cell_move_8_9.is_discover[0] = False

    # discovered cell with arrow
    cell_move_7_8 = Cell(7, 8)
    cell_move_7_8.arrow = 1
    cell_move_7_8.is_discover[0] = True

    # covered cell with opponent charatcer
    cell_move_9_8 = Cell(9, 8)
    cell_move_9_8.character = opponent_player.characters[1]
    cell_move_9_8.is_discover[0] = False

    # moving character 3
    cell_move_0_0 = Cell(0, 0)
    cell_move_0_0.character = moving_player.characters[3]
    cell_move_0_0.is_discover[0] = True
    return [cell_move_4_4, cell_move_4_3, cell_move_4_5,
            cell_move_3_4, cell_move_5_4, cell_move_8_8,
            cell_move_8_7, cell_move_8_9, cell_move_7_8,
            cell_move_9_8, cell_move_0_0]
