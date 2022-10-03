# PLAYER
CHARACTER_AMOUNT_PER_PLAYER = 3
INITIAL_ARROWS = 6
INITIAL_SCORE = 0
PLAYER_1 = 'L'
PLAYER_2 = 'R'
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

# Users
NAME_USER_1 = 'name1'
NAME_USER_2 = 'name2'

# constants_game
LARGE = 17
MIDDLE = 8
GOLD_QUANTITY = 16
GOLD = 'GOLD'
DIAMOND = 'DIAMOND'
HOLE = 'O'
HOLE_QUANTITY = 16
EMPTY_STRING = ''

# constants_scores
CORRECT_MOVE = "CORRECT_MOVE"
INVALID_MOVE = "INVALID_MOVE"
KILL = "KILL"
ARROW_MISS = "ARROW_MISS"
GET_ITEMS = "GET_ITEMS"
TIMEOUT_SC = "TIMEOUT"
DEATH = "DEATH"

SCORES = {
    CORRECT_MOVE: 1000,
    INVALID_MOVE: -1000,
    GOLD: 10000,
    DIAMOND: 60000,
    KILL: 15000,
    ARROW_MISS: 1000,
    TIMEOUT_SC: -1000
}

# constants_messages
GAME_OVER_MESSAGE_1 = "GAME OVER - Player 1 reached 5 invalid moves in a row"
GAME_OVER_MESSAGE_2 = "GAME OVER - Player 2 reached 5 invalid moves in a row"
GAME_OVER_MESSAGE_3 = "GAME OVER - DRAW. No turns left and scores are the same."
GAME_OVER_MESSAGE_4 = "GAME OVER - Player 1 has no living Characters..."
GAME_OVER_MESSAGE_5 = "GAME OVER - Player 2 has no living Characters..."
GAME_OVER_MESSAGE_6 = "GAME OVER - No turns left - Player 1 wins by score difference"
GAME_OVER_MESSAGE_7 = "GAME OVER - No turns left - Player 2 wins by score difference"
GAME_OVER_NOT_MET = "Game comtinues..."
