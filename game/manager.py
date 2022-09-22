from game.game import WumpusGame
from constans.constans import (
    ACTION,
    COL,
    DATA,
    DIRECTION_MESSAGE,
    # GAMEOVER_STATE,
    # INVALID_PENALIZE,
    MESSAGE_DATA_KEYS,
    POSIBLE_ACTIONS,
    POSIBLE_DIRECTIONS,
    ROW,
    # STATE,
    # TIMEOUT
)

from exceptions.personal_exceptions import (
    InvalidData,
    InvalidKey,
    InvalidQuantityPlayers
)

from typing import List
from edagames_grpc.game_start import GameStart


class Manager():
    def __init__(self) -> None:
        self.games = dict()
        self.action_data = dict()

    def get_correct_data(self, data, data_keys):
        try:
            message = {}
            for key in data_keys:
                value = data[key]
                if value in POSIBLE_DIRECTIONS:
                    message[key] = value
                elif key != DIRECTION_MESSAGE and type(value) != bool:
                    message[key] = int(value)
                else:
                    raise InvalidData()
            return message
        except KeyError:
            raise InvalidKey()
        except ValueError:
            raise InvalidData()

    def execute_action_manager(self, game: WumpusGame, api_data: dict()):
        if ACTION in api_data and api_data[ACTION] in POSIBLE_ACTIONS:
            self.action_data = self.get_correct_data(
                api_data[DATA],
                MESSAGE_DATA_KEYS
            )
            game.execute_action(
                api_data[ACTION],
                api_data[DATA][ROW],
                api_data[DATA][COL],
                api_data[DATA][DIRECTION_MESSAGE],
            )
        else:
            raise InvalidData()

    def delete_game_from_manager(self, game_id: str) -> None:
        del self.games[game_id]

    def check_game_over(self, current_game):
        if current_game.remaining_moves <= 0 or not current_game.game_is_active:
            self.delete_game_from_manager(current_game.game_id)
            return True
        else:
            return False

    # TO DO
    # def penalize(self, game_id: str) -> GameState:
    #     current_game = self.games[game_id]
    #     current_game.penalize_player()
    #     current_game.next_turn()
    #     state = TIMEOUT
    #     if self.check_game_over(current_game):
    #         state = GAMEOVER_STATE
    #     self.action_data = INVALID_PENALIZE
    #     return self.get_game_state(
    #         current_game,
    #         state,
    #     )
    # TO DO
    # def get_game_state(
    #     self,
    #     game: WumpusGame,
    #     state: str,
    # ) -> GameState:
    #     play_data = game.get_play_data(self.action_data)
    #     play_data[STATE] = state
    #     return GameState(
    #         game.game_id,
    #         game.get_current_player_name(),
    #         game.get_turn_data(),
    #         play_data,
    #     )
    def create_game(self, users_names: List[str]) -> GameStart:
        if len(users_names) in [2, 4]:
            new_game = WumpusGame(users_names)
            return self.get_game_start(new_game)
        else:
            raise InvalidQuantityPlayers()

    def get_game_start(self, game: WumpusGame) -> GameStart:
        return GameStart(
            game.game_id,
            game.get_current_player_name(),
            game.generate_response(),
        )
