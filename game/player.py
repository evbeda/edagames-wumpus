from constans.constans import (
    INITIAL_ARROWS,
    INITIAL_SCORE,
    CHARACTER_AMOUNT_PER_PLAYER,
)
from game.character import Character


class Player():

    def __init__(self, name):
        self.name = name
        self.score = INITIAL_SCORE
        self.arrows = INITIAL_ARROWS
        self.characters = []
        self.instance_characters()

    def update_score(self, new_score):
        self.score += new_score

    def update_arrows(self, new_arrow_amt):
        self.arrows += new_arrow_amt

    def instance_characters(self):
        for _ in range(CHARACTER_AMOUNT_PER_PLAYER):
            self.characters.append(Character(self.name))
