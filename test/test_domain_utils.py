import unittest
from constants.constants import (
    EAST,
    NAME_USER_1,
    NAME_USER_2,
    NORTH,
    PLAYER_1,
    PLAYER_2,
    SOUTH,
    WEST,
)
from constants.scenarios_shoot import board_friendly_fire_player_1, board_friendly_fire_player_2
from application.utils import (
    is_a_player_character,
    is_frendly_fire,
    target_position_within_bounds,
    there_are_arrows_available,
)
from game.board import Board
from game.game import WumpusGame
from game.player import Player
from parameterized import parameterized
from unittest.mock import patch


def patched_game() -> WumpusGame:
    with patch.object(Board, '_valid_hole', return_value=True):
        users_name = [NAME_USER_1, NAME_USER_2]
        game = WumpusGame(users_name)
    return game


class TestUtils(unittest.TestCase):

    @parameterized.expand([
        (Player(PLAYER_1, NAME_USER_1), 0, False),
        (Player(PLAYER_1, NAME_USER_1), 1, True),
        (Player(PLAYER_1, NAME_USER_1), 5, True),
        (Player(PLAYER_2, NAME_USER_2), 0, False),
        (Player(PLAYER_2, NAME_USER_2), 1, True),
        (Player(PLAYER_2, NAME_USER_2), 6, True),
     ])
    def test_no_arrows_availabe(self, player, arrows, expected):
        current_player = player
        current_player.arrows = arrows
        result = there_are_arrows_available(current_player)
        self.assertEqual(result, expected)

    @parameterized.expand([
        (board_friendly_fire_player_1(), Player(PLAYER_1, NAME_USER_1), 0, 0, EAST, True),
        (board_friendly_fire_player_1(), Player(PLAYER_1, NAME_USER_1), 8, 0, NORTH, False),
        (board_friendly_fire_player_2(), Player(PLAYER_2, NAME_USER_2), 0, 16, WEST, True),
        (board_friendly_fire_player_2(), Player(PLAYER_2, NAME_USER_2), 8, 16, SOUTH, False)
     ])
    def test_friendly_fire(self, board, current_player, row, col, direction, expected):
        game = patched_game()
        game._board._board = board
        current_player = current_player
        result = is_frendly_fire(row, col, direction, current_player, game._board)
        self.assertEqual(result, expected)

    @parameterized.expand(
        [
            (0, 0, NORTH),
            (0, 0, WEST),
            (16, 16, SOUTH),
            (16, 16, EAST)
        ]
    )
    def test_target_position_within_bounds_exception(self, row, col, direction):
        self.assertFalse(target_position_within_bounds(row, col, direction))

    @parameterized.expand(
        [
            (0, 0, SOUTH, (1, 0)),
            (0, 0, EAST, (0, 1)),
            (16, 16, NORTH, (15, 16)),
            (16, 16, WEST, (16, 15))
        ]
    )
    def test_target_position_ok(self, row, col, direction, expected):
        result = target_position_within_bounds(row, col, direction)
        self.assertEqual(result, expected)

    @parameterized.expand(
        [
            (0, 0, True),
            (8, 0, True),
            (16, 0, True),
            (0, 16, False),
            (8, 16, False),
            (16, 16, False)
        ]
    )
    def test_is_a_player_character_player_1(self, row, col, expected_result):
        game = patched_game()
        game.current_player = Player(PLAYER_1, NAME_USER_1)
        result = is_a_player_character(row, col, game.current_player, game._board)
        self.assertEqual(result, expected_result)

    @parameterized.expand(
        [
            (0, 0, False),
            (8, 0, False),
            (16, 0, False),
            (0, 16, True),
            (8, 16, True),
            (16, 16, True)
        ]
    )
    def test_is_a_player_character_player_2(self, row, col, expected_result):
        game = patched_game()
        game.current_player = Player(PLAYER_2, NAME_USER_2)
        result = is_a_player_character(row, col, game.current_player, game._board)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
