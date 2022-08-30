class Character:

    def __init__(self, player) -> None:
        self.golds = 0
        self.diamonds = 0
        self.player = player

    def __str__(self):
        return (f"gold: {self.golds}, player: {self.player}, " +
                f"diamonds: {self.diamonds}.")
