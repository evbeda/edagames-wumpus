from constans.constans import (
    DIRECTION_MESSAGE,
    POSIBLE_DIRECTIONS,
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
