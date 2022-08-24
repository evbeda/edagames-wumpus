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


if __name__ == '__main__':
    unittest.main()
