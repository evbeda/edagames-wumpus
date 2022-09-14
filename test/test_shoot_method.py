import unittest
from parameterized import parameterized
from game.character import Character
from game.diamond import Diamond

from game.game import WumpusGame

from constans.constans import INITIAL_ARROWS
from constans.constants_utils import NORTH, SOUTH, EAST, WEST
from exceptions.personal_exceptions import (
                                           noArrowsAvailableException,
                                           friendlyFireException,
                                           shootOutOfBoundsException)

from game.gold import Gold


class Test_shoot(unittest.TestCase):

    def test_no_arrows_to_shoot(self):
        game = WumpusGame()
        game.current_player.arrows = 0
        with self.assertRaises(noArrowsAvailableException):
            game.shoot_arrow(0, 0, EAST)

    def test_arrow_decrease(self):
        game = WumpusGame()
        game.shoot_arrow(0, 0, EAST)
        self.assertEqual(game.current_player.arrows, INITIAL_ARROWS - 1)

    @parameterized.expand(
        [
            (0, 0, WEST),
            (0, 0, NORTH),
            (16, 16, EAST),
            (16, 16, SOUTH)
        ]
    )
    def test_target_out_of_bounds(self, row, col, direction):
        game = WumpusGame()
        with self.assertRaises(shootOutOfBoundsException):
            game.target_position(row, col, direction)

    @parameterized.expand(
        [
            (0, 0, EAST, (0, 1)),
            (0, 0, SOUTH, (1, 0)),
            (16, 16, WEST, (16, 15)),
            (16, 16, NORTH, (15, 16))
        ]
    )
    def test_target_in_bounds(self, row, col, direction, expected):
        game = WumpusGame()
        result = game.target_position(row, col, direction)
        self.assertEqual(result, expected)

    def test_shoot_own_character(self):
        game = WumpusGame()
        character = Character(game.current_player)
        game._board[0][1].character = character
        with self.assertRaises(friendlyFireException):
            game.shoot_arrow(0, 0, EAST)

    def test_kill_opp(self):
        row = 0
        col = 1
        game = WumpusGame()
        opp_character = Character(game.player_2)
        opp_character.treasures.append(Diamond())
        opp_character.treasures.append(Gold())
        opp_character.treasures.append(Gold())
        game._board[row][col].treasures = []
        game._board[row][col].character = opp_character
        opp_cell = game._board[row][col]
        game.kill_opp(row, col)
        self.assertEqual(opp_cell.diamond, 1)
        self.assertEqual(opp_cell.gold, 2)
        self.assertEqual(opp_cell.character, None)
        self.assertTrue(opp_cell.is_discover[0])

    def test_shoot_miss(self):
        game = WumpusGame()
        row = 0
        col = 1
        target_cell = game._board[row][col]
        current_player = game.current_player
        game.shoot_miss(row, col)
        self.assertEqual(target_cell.arrow, 1)
        self.assertEqual(current_player.arrows, INITIAL_ARROWS - 1)
        self.assertTrue(target_cell.is_discover[0])

    def test_shoot_into_hole(self):
        game = WumpusGame()
        row = 0
        col = 1
        target_cell = game._board[row][col]
        current_player = game.current_player
        game.shoot_hole(row, col)
        self.assertEqual(current_player.arrows, INITIAL_ARROWS - 1)
        self.assertTrue(target_cell.is_discover[0])

    def test_shoot_n_kill(self):
        game = WumpusGame()
        opp_character = Character(game.player_2)
        opp_character.treasures.append(Diamond())
        opp_character.treasures.append(Gold())
        opp_character.treasures.append(Gold())
        game._board[0][1].treasures = []
        game._board[0][1].character = opp_character
        game.shoot_arrow(0, 0, EAST)
        self.assertEqual(len(game._board[0][1].treasures), 3)
        self.assertEqual(game._board[0][1].character, None)
        self.assertTrue(game._board[0][1].is_discover[0])
        self.assertEqual(game.current_player.arrows, INITIAL_ARROWS - 1)

    def test_shoot_hole(self):
        game = WumpusGame()
        game._board[0][1].has_hole = True
        game.shoot_arrow(0, 0, EAST)
        self.assertEqual(game.current_player.arrows, INITIAL_ARROWS - 1)
        self.assertTrue(game._board[0][1].is_discover[0])


if __name__ == '__main__':
    unittest.main()
