
from game.TresaureHolder import TreasureHolder
# from game.diamond import Diamond
# from game.gold import Gold


class Character(TreasureHolder):

    def __init__(self, player) -> None:
        super().__init__()
        self.player = player

    def __str__(self):
        return (f"gold: {self.gold}, player: {self.player}, " +
                f"diamonds: {self.diamond}.")
