from game.treasure import Treasure
from constans.constants_scores import scores


class Gold(Treasure):
    def __init__(self) -> None:
        super().__init__()
        self.value = scores["GOLD"]
