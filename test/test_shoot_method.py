import unittest
from parameterized import parameterized
from game.character import Character

from game.game import WumpusGame
from game.player import Player
from utils.shoot_utils import (shoot_arrow,
                               target_position,
                               kill_opp,
                               shoot_miss
                               )
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

    def test_reveal_cell_p1(self):
        row = 1
        col = 1
        game = WumpusGame()
        game.discover_cell(row, row)
        result = game._board[row][col].is_discover_by_player_1
        self.assertEqual(result, True)

    def test_reveal_cell_p2(self):
        row = 1
        col = 1
        game = WumpusGame()
        game.change_current_player()
        game.discover_cell(row, col)
        result = game._board[row][col].is_discover_by_player_2
        self.assertEqual(result, True)

    def test_kill_opp(self):
        row = 0
        col = 1
        game = WumpusGame()
        opp_character = Character(game.player_2)
        opp_character.diamonds = 1
        opp_character.golds = 2
        game._board[row][col].character = opp_character
        opp_cell = game._board[row][col]
        kill_opp(row, col, game)
        self.assertEqual(opp_cell.diamond, 1)
        self.assertEqual(opp_cell.gold, 2)
        self.assertEqual(opp_cell.character, None)
        self.assertTrue(opp_cell.is_discover_by_player_1)

    def test_shoot_miss(self):
        game = WumpusGame()
        row = 0
        col = 1
        shoot_miss(row, col, game)
        target_cell = game._board[row][col]
        current_player = game.current_player
        self.assertEqual(target_cell.arrow, 1)
        self.assertEqual(current_player.arrows, INITIAL_ARROWS - 1)
        self.assertTrue(target_cell.is_discover_by_player_1)


if __name__ == '__main__':
    unittest.main()
