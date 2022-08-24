import unittest
from parameterized import parameterized
from game.player import Player
from constans.constans import (
    INITIAL_ARROWS,
    INITIAL_SCORE,
)


class TestPlayer(unittest.TestCase):

    @parameterized.expand([
        (INITIAL_ARROWS, INITIAL_SCORE),
    ])
    def test_player_init(self, expected_arrows, expected_score):
        self.player = Player()
        self.assertEqual(self.player.arrows, expected_arrows)
        self.assertEqual(self.player.score, expected_score)


if __name__ == '__main__':
    unittest.main()
