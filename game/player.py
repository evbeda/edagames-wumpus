from constans.constans import (
    INITIAL_ARROWS,
    INITIAL_SCORE,
)


class Player():

    def __init__(self, name):
        self.name = name
        self.score = INITIAL_SCORE
        self.arrows = INITIAL_ARROWS
        self.strike_counter = 0

    def update_score(self, new_score):
        self.score += new_score

    def update_arrows(self, new_arrow_amt):
        self.arrows += new_arrow_amt

    def strike_counter_increment(self):
        self.strike_counter += 1
