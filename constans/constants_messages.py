from constans.scenarios import SCENARIO_STR_PLAYER_1
from constans.constans import (
    INITIAL_ARROWS
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
    "event": "your_turn",
    "data": {
        "board": SCENARIO_STR_PLAYER_1,
        "game_active": True,
        "remaining_turns": 200,
        #  "game_id": "12345678" Add when self.game_id is ready
        "side": "B",  # Will be "B" or "P"
        "your_player": {
            "score": 0,
            "arrows": INITIAL_ARROWS,
            "owner": 'matias'
        },
        "enemy_player": {
            "name": "P",  # Will be "B" or "P"
            "score": 0,
            "arrows": INITIAL_ARROWS,
            "owner": 'guille'
        }
    }
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
