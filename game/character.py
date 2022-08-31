
from game.TresaureHolder import TreasureHolder
# from game.diamond import Diamond
# from game.gold import Gold


class Character(TreasureHolder):

    def __init__(self, player) -> None:

        # TODO
        # [ ] delete self.golds and migrate to the function
        # [ ] delete self.diamonds and migrate to the function

        super().__init__()

        self.golds = 0
        self.diamonds = 0
        self.player = player

    def __str__(self):
        return (f"gold: {self.golds}, player: {self.player}, " +
                f"diamonds: {self.diamonds}.")
