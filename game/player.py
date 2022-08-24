from constans.constans import (
    INITIAL_ARROWS,
    INITIAL_SCORE,
)


class Player():

    def __init__(self, name):
        self.name = name
        self.score = INITIAL_SCORE
        self.arrows = INITIAL_ARROWS
