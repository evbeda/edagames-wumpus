class Cell():
    def __init__(self, row, col):
        self.position: tuple(row, col)
        self.gold = 0
        self.diamond = 0
        self.character = None
        self.has_hole = False
        self.is_discover_by_player_1 = False
        self.is_discover_by_player_2 = False
        self.arrow = 0

    @property
    def empty(self) -> bool:
        return not (self.gold or self.diamond
                    or self.character or self.has_hole
                    or self.arrow)

    @property
    def are_there_player(self) -> bool:
        return self.character is not None

    # TODO: refactor method
    def set_character_when_move(self, character):
        self.character = character
        self.gold = character.golds
        self.diamond = character.diamonds
