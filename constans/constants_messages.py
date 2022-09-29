from constans.scenarios import SCENARIO_STR_PLAYER_1
from constans.constans import (
    INITIAL_ARROWS,
    NAME_USER_1,
    NAME_USER_2,
)

GAME_OVER_MESSAGE_1 = "GAME OVER - Player 1 reached 5 invalid moves in a row"
GAME_OVER_MESSAGE_2 = "GAME OVER - Player 2 reached 5 invalid moves in a row"
GAME_OVER_MESSAGE_3 = "GAME OVER - DRAW. No turns left and scores are the same."
GAME_OVER_MESSAGE_4 = "GAME OVER - Player 1 has no living Characters..."
GAME_OVER_MESSAGE_5 = "GAME OVER - Player 2 has no living Characters..."
GAME_OVER_MESSAGE_6 = "GAME OVER - No turns left - Player 1 wins by score difference"
GAME_OVER_MESSAGE_7 = "GAME OVER - No turns left - Player 2 wins by score difference"
GAME_OVER_NOT_MET = "Game comtinues..."

RESPONSE_1 = {
    "status": GAME_OVER_MESSAGE_4,
    "winner_side": "P",
    'score': {
        'player_1': -100,
        'player_2': 0,
    },
    'result': {
        'WINNER': NAME_USER_2,
        'LOSER': NAME_USER_1,
    }
}

RESPONSE_2 = {
    "player_2": NAME_USER_2,
    "player_1": NAME_USER_1,
    "score_1": 0,
    "score_2": 0,
    "arrows_1": INITIAL_ARROWS,
    "arrows_2": INITIAL_ARROWS,
    "board": SCENARIO_STR_PLAYER_1,
    "remaining_turns": 200,
    "game_id": "1234-5678-9012-3456-7890",
    "side": "B",  # Will be "B" or "P"
}

RESPONSE_3 = {
    "status": GAME_OVER_MESSAGE_5,
    "winner_side": "B",
    'score': {
        'player_1': 0,
        'player_2': -100,
    },
    'result': {
        'WINNER': NAME_USER_1,
        'LOSER': NAME_USER_2,
    }
}

RESPONSE_4 = {
    "status": GAME_OVER_MESSAGE_3,
    "winner_side": "DRAW",
    'score': {
        'player_1': 0,
        'player_2': 0,
    },
    'result': "DRAW",
}

RESPONSE_6 = {
    "status": GAME_OVER_MESSAGE_6,
    "winner_side": "B",
    'score': {
        'player_1': 5000,
        'player_2': 1000,
    },
    'result': {
        'WINNER': NAME_USER_1,
        'LOSER': NAME_USER_2,
    }
}

RESPONSE_7 = {
    "status": GAME_OVER_MESSAGE_7,
    "winner_side": "P",
    'score': {
        'player_1': 1000,
        'player_2': 5000,
    },
    'result': {
        'WINNER': NAME_USER_2,
        'LOSER': NAME_USER_1,
    }
}
