class Cell():
    def __init__(self):
        self.position: tuple()
        self.gold = 0
        self.diamond = 0
        self.character = None
        self.has_hole = False
        self.is_discover = False
        self.arrow = 0

    @property
    def emty(self) -> bool:
        return not (self.gold or self.diamond
                    or self.character or self.has_hole
                    or self.arrow)

    def set_character_initial_pos(self, character):
        self.character = character

    def set_character_when_move(self, character):
        self.character = character
        self.gold = character.golds
        self.diamond = character.diamonds
