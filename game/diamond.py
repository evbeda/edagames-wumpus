from constans.constans import SCORES
from game.treasure import Treasure


class Diamond(Treasure):
    def __init__(self) -> None:
        super().__init__()
        self.value = SCORES["DIAMOND"]
