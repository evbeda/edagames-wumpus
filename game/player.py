from constans.constans import (
    INITIAL_ARROWS,
    INITIAL_SCORE,
    CHARACTER_AMOUNT_PER_PLAYER,
)
from constans.constants_game import DIAMOND, GOLD
from constans.constants_scores import SCORES
from game.character import Character


class Player():

    def __init__(self, name):
        self.name = name
        self._score = INITIAL_SCORE
        self.arrows = INITIAL_ARROWS
        self.characters = []
        self.instance_characters()

    def update_score(self, new_score):
        self.score += new_score

    def update_arrows(self, new_arrow_amt):
        self.arrows += new_arrow_amt

    def instance_characters(self):
        for _ in range(CHARACTER_AMOUNT_PER_PLAYER):
            self.characters.append(Character(self))

    @property
    def score(self):
        gold_score = sum([chracter.gold
                          for chracter in self.characters]) * SCORES[GOLD]
        diamond_score = sum([chracter.diamond
                             for chracter in self.characters]
                            ) * SCORES[DIAMOND]
        return self._score + gold_score + diamond_score

    @score.setter
    def score(self, score):
        self._score = score
