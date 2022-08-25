import unittest
from parameterized import parameterized
from game.character import Character

from game.game import WumpusGame
from game.player import Player
from utils.shoot_utils import shoot_arrow, target_position
from constans.constans import PLAYER_1, INITIAL_ARROWS
from constans.constants_utils import NORTH, SOUTH, EAST, WEST


class Test_shoot(unittest.TestCase):

    def test_no_arrows_to_shoot(self):
        game = WumpusGame()
        player = Player(PLAYER_1)
        player.arrows = 0
        game.player_1 = player
        with self.assertRaises(Exception):
            shoot_arrow(game.player_1, 0, 0, EAST, game)

    def test_arrow_decrease(self):
        game = WumpusGame()
        player = Player(PLAYER_1)
        game.player_1 = player
        character = Character(player)
        game._board[0][0].character = character
        shoot_arrow(player, 0, 0, WEST, game)
        self.assertEqual(player.arrows, INITIAL_ARROWS - 1)

    @parameterized.expand(
        [
            (0, 0, EAST),
            (0, 0, NORTH),
            (16, 16, WEST),
            (16, 16, SOUTH)
        ]
    )
    def test_target_out_of_bounds(self, row, col, direction):
        with self.assertRaises(Exception):
            target_position(row, col, direction)

    @parameterized.expand(
        [
            (0, 0, WEST, (0, 1)),
            (0, 0, SOUTH, (1, 0)),
            (16, 16, EAST, (16, 15)),
            (16, 16, NORTH, (15, 16))
        ]
    )
    def test_target_in_bounds(self, row, col, direction, expected):
        result = target_position(row, col, direction)
        self.assertEqual(result, expected)

    def test_shoot_own_character(self):
        game = WumpusGame()
        player = Player(PLAYER_1)
        game.player_1 = player
        character = Character(player)
        game._board[0][1].character = character

        with self.assertRaises(Exception):
            shoot_arrow(player, 0, 0, WEST, game)


if __name__ == '__main__':
    unittest.main()
