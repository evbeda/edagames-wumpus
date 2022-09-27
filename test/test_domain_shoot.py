import unittest
from constans.constans import (
    EAST,
    NAME_USER_1,
    NAME_USER_2,
    NORTH,
    PLAYER_1,
    PLAYER_2,
    SOUTH,
    WEST,
)
from constans.scenarios import board_friendly_fire_player_1, board_friendly_fire_player_2

from application.shoot_arrow import ShootArrow
from game.board import Board
from game.player import Player
from game.game import WumpusGame
from exceptions.personal_exceptions import (
    friendlyFireException,
    noArrowsAvailableException,
    notYourCharacterException,
    shootOutOfBoundsException,
)
from parameterized import parameterized
from unittest.mock import patch


def patched_game() -> WumpusGame:
    with patch.object(Board, '_valid_hole', return_value=True):
        users_name = [NAME_USER_1, NAME_USER_2]
        game = WumpusGame(users_name)
    return game


class TestShootActions(unittest.TestCase):

    @parameterized.expand([
        (0, 0, 0, EAST, Player(PLAYER_1, NAME_USER_1)),
        (0, 8, 0, NORTH, Player(PLAYER_1, NAME_USER_1)),
        (0, 0, 16, WEST, Player(PLAYER_2, NAME_USER_2)),
        (0, 16, 16, NORTH, Player(PLAYER_2, NAME_USER_2)),
    ])
    def test_show_arrow_no_arrows_raise_exception(self, arrows, row, col, direction, player):
        game = patched_game()
        current_player = player
        current_player.arrows = arrows
        shoot_arrow = ShootArrow()
        with self.assertRaises(noArrowsAvailableException):
            shoot_arrow.execute(row, col, direction, current_player, game._board)

    @parameterized.expand([
        (board_friendly_fire_player_1(), Player(PLAYER_1, NAME_USER_1), 0, 0, EAST),
        (board_friendly_fire_player_2(), Player(PLAYER_2, NAME_USER_2), 0, 16, WEST),
    ])
    def test_shoot_own_character(self, board, player, row, col, direction):
        game = patched_game()
        game._board._board = board
        current_player = player
        shoot_arrow = ShootArrow()
        with self.assertRaises(friendlyFireException):
            shoot_arrow.execute(row, col, direction, current_player, game._board)

    @parameterized.expand(
        [
            (0, 0, NORTH),
            (0, 0, WEST),
            (16, 16, SOUTH),
            (16, 16, EAST)
        ]
    )
    def test_target_position_exception(self, row, col, direction):
        game = patched_game()
        shoot_arrow = ShootArrow()
        with self.assertRaises(shootOutOfBoundsException):
            shoot_arrow.execute(row, col, direction, game.current_player, game._board)

    @parameterized.expand(
        [
            (0, 1, EAST),
            (0, 1, SOUTH),
            (16, 15, WEST),
            (16, 7, NORTH)
        ]
    )
    def test_shoot_not_your_character_exception(self, row, col, direction):
        game = patched_game()
        shoot_arrow = ShootArrow()
        with self.assertRaises(notYourCharacterException):
            shoot_arrow.execute(row, col, direction, game.current_player, game._board)
