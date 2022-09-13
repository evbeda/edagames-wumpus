from __future__ import annotations
from game.gold import Gold
from game.diamond import Diamond


class TreasureHolder:

    def __init__(self) -> None:
        self.treasures = list()

    def transfer_tresaure(self, other: TreasureHolder) -> None:
        other.treasures.extend(self.treasures)
        self.drop_treasures()

    def drop_treasures(self):
        self.treasures = []

    @property
    def gold(self):
        return len([tresaure
                    for tresaure in self.treasures
                    if type(tresaure) == Gold])

    @property
    def diamond(self):
        return len([tresaure
                    for tresaure in self.treasures
                    if type(tresaure) == Diamond
                    ])
