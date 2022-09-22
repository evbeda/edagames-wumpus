from game.game import WumpusGame
from constans.constans import (
    ACTION,
    COL,
    DATA,
    DIRECTION_MESSAGE,
    MESSAGE_DATA_KEYS,
    POSIBLE_ACTIONS,
    POSIBLE_DIRECTIONS,
    ROW
)
from exceptions.personal_exceptions import (
    InvalidData,
    InvalidKey
)


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
