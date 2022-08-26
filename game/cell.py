from constans.constans import PLAYER_1
from constans.constants_game import HOLE


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

    @property
    def has_player(self):
        return self.character.player.name if (
            self.character is not None
            ) else None

    def to_str(self, player_name):

        if player_name == PLAYER_1:
            discovered = self.is_discover_by_player_1
        else:
            discovered = self.is_discover_by_player_2

        if not discovered:
            representation = ['#']*5
            if self.arrow:
                representation[2] = 'F'

        else:
            representation = [' ']*5
            self._middle_char(representation)
            self._put_treasure(representation)

        return ''.join(representation)

    def _middle_char(self, representation: list):
        if self.character:
            representation[2] = self.character.player.name

        elif self.has_hole:
            representation[2] = HOLE

        elif self.arrow:
            representation[2] = 'F'

    def _put_treasure(self, representation: list):
        if self.gold:
            representation[1] = str(self.gold)
        if self.diamond:
            representation[-2] = 'D'
