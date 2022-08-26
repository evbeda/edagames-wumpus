import unittest
from parameterized import parameterized
from game.player import Player
from constans.constans import (
    PLAYER_1,
    PLAYER_2,
    INITIAL_ARROWS,
    INITIAL_SCORE,
)


class TestPlayer(unittest.TestCase):

    @parameterized.expand([
        (PLAYER_1, INITIAL_ARROWS, INITIAL_SCORE),
        (PLAYER_2, INITIAL_ARROWS, INITIAL_SCORE),
    ])
    def test_player_init(self, name, expected_arrows, expected_score):
        self.player = Player(name)
        self.assertEqual(self.player.arrows, expected_arrows)
        self.assertEqual(self.player.score, expected_score)
        self.assertEqual(self.player.name, name)

    @parameterized.expand([
        (PLAYER_1, 0, -10000, -10000),
        (PLAYER_2, 5000, 10000, 15000),
    ])
    def test_update_score(self, player_name,
                          actual_score, score_mod, expected_result):
        self.player = Player(player_name)
        self.player.score = actual_score
        self.player.update_score(score_mod)
        self.assertEqual(self.player.score, expected_result)

    @parameterized.expand([
        (PLAYER_1, 4, -1, 3),
        (PLAYER_2, 0, 1, 1),
    ])
    def test_update_arrows(self, player_name,
                           actual_arrows, arrows_mod, expected_result):
        self.player = Player(player_name)
        self.player.arrows = actual_arrows
        self.player.update_arrows(arrows_mod)
        self.assertEqual(self.player.arrows, expected_result)

    @parameterized.expand([
        (PLAYER_1, 1, 2),
    ])
    def test_strike_counter_increment(self, player_name,
                                      actual, expected_result):
        player = Player(player_name)
        player.strike_counter = actual
        player.strike_counter_increment()
        self.assertEqual(player.strike_counter, expected_result)


if __name__ == '__main__':
    unittest.main()
