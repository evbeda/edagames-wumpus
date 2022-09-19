from constans.constans import PLAYER_1
from constans.constants_game import HOLE
from game.TresaureHolder import TreasureHolder


class Cell(TreasureHolder):

    def __init__(self, row, col):
        super().__init__()
        self.position = (row, col)
        self.character = None
        self.has_hole = False
        # self.is_discover_by_player_1 = False
        # self.is_discover_by_player_2 = False
        self.is_discover = [False, False]
        # self.gold = 0
        # self.diamond = 0
        self.arrow = 0

    @property
    def empty(self) -> bool:
        return not (self.treasures
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

    def to_str(self, player_name: str):

        if player_name == PLAYER_1:
            discovered = self.is_discover[0]
        else:
            discovered = self.is_discover[1]

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

    def remove_character(self) -> None:
        player = self.character.player
        player.characters.remove(self.character)
        self.character = None

    def put_hole(self):
        self.has_hole = True

    def remove_hole(self):
        self.has_hole = False
