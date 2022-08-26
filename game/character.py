from game.player import Player


class Character:

    def __init__(self, player: Player) -> None:
        self.golds = 0
        self.diamonds = 0
        self.player = player
