from constans.scenarios import SCENARIO_STR_PLAYER_1
from constans.constans import (
    INITIAL_ARROWS,
    NAME_USER_1,
    NAME_USER_2
)

GAME_OVER_MESSAGE_1 = "GAME OVER - Player 1 reached 5 invalid moves in a row"
GAME_OVER_MESSAGE_2 = "GAME OVER - Player 2 reached 5 invalid moves in a row"
GAME_OVER_MESSAGE_3 = "GAME OVER - No turns left"
GAME_OVER_MESSAGE_4 = "GAME OVER - Player 1 has no living Characters..."
GAME_OVER_MESSAGE_5 = "GAME OVER - Player 2 has no living Characters..."
GAME_OVER_NOT_MET = "Game comtinues..."

RESPONSE_1 = {
    "event": "GAME_OVER",
    "data": {
        "status": GAME_OVER_MESSAGE_4,
        'SCORE': {
            'B': -100,
            'P': 0,
        },
        'RESULT': {
            'WINNER': 'P',
            'LOSER': 'B',
        }
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
    "game_active": True,
    "remaining_turns": 200,
    "game_id": "1234-5678-9012-3456-7890",
    "side": "B",  # Will be "B" or "P"
}

RESPONSE_3 = {
    "event": "GAME_OVER",
    "data": {
        "status": GAME_OVER_MESSAGE_5,
        'SCORE': {
            'B': 0,
            'P': -100,
        },
        'RESULT': {
            'WINNER': 'B',
            'LOSER': 'P',
        }
    }
}
