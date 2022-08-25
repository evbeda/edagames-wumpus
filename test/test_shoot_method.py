import unittest

from game.game import WumpusGame
from game.player import Player
from utils.shoot_utils import shoot_arrow


class Test_shoot(unittest.TestCase):

    def setUp(self):
        pass

    def test_no_arrows_to_shoot(self):
        game = WumpusGame()
        player = Player("Char1")
        player.arrows = 0
        game.player_1 = player
        with self.assertRaises(Exception):
            shoot_arrow(game.player_1, (0, 0), "A")


if __name__ == '__main__':
    unittest.main()
