from constants.constants import SCORES
from game.treasure import Treasure


class Gold(Treasure):
    def __init__(self) -> None:
        super().__init__()
        self.value = SCORES["GOLD"]
