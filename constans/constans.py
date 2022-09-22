# PLAYER
CHARACTER_AMOUNT_PER_PLAYER = 3
INITIAL_ARROWS = 6
INITIAL_SCORE = 0
PLAYER_1 = 'B'
PLAYER_2 = 'P'
INITIAL_POSITION_PLAYER_1 = [(0, 0), (8, 0), (16, 0)]
INITIAL_POSITION_PLAYER_2 = [(0, 16), (8, 16), (16, 16)]
INITIAL_POSITIONS = INITIAL_POSITION_PLAYER_1 + INITIAL_POSITION_PLAYER_2
CLOSE_AREA_PLAYER_1 = [(1, 0), (0, 1), (7, 0), (9, 0), (8, 1),
                       (15, 0), (16, 1)]
CLOSE_AREA__PLAYER_2 = [(0, 15), (1, 16), (7, 16), (9, 16), (8, 15),
                        (15, 16), (16, 15)]

FORBIDDEN_HOLE_CELLS = (INITIAL_POSITIONS +
                        CLOSE_AREA_PLAYER_1 + CLOSE_AREA__PLAYER_2)

EMPTY_CELL = '     '
HIDDEN_CELL = '#####'

JOIN_ROW_BOARD = ''

MAXIMUM_INVALID_MOVES = 5
INVALID_MOVES_SCORE = -9999

NORTH = "NORTH"
SOUTH = "SOUTH"
EAST = "EAST"
WEST = "WEST"
MOVE = "MOVE"
SHOOT = "SHOOT"

ACTION = "action"

DATA = "data"

DIRECTION_MESSAGE = 'direction'

ROW = 'from_row'

COL = 'from_col'

MESSAGE_DATA_KEYS = [ROW, COL, DIRECTION_MESSAGE]

POSIBLE_DIRECTIONS = [NORTH, SOUTH, EAST, WEST]

POSIBLE_ACTIONS = [MOVE, SHOOT]

# States
VALID_STATE = 'valid'
INVALID_STATE = 'invalid'
GAMEOVER_STATE = 'gameover'
ABORT = 'game aborted'
TIMEOUT = 'timeout'
STATE = 'state'

# Invalid penalize

INVALID_PENALIZE = {'from_row': 'invalid', 'from_col': 'invalid', 'direction': 'invalid'}
NAME_USER_1 = 'name1'
NAME_USER_2 = 'name2'
