from application.shoot_arrow import ShootArrow
from application.shoot_to_hole import ShootToHole
from application.utils import target_position_within_bounds
from constans.constans import (
    EAST,
    INITIAL_ARROWS,
    NAME_USER_1,
    NAME_USER_2,
    NORTH,
    PLAYER_1,
    PLAYER_2,
    SOUTH,
    WEST,
)
from constans.constants_scores import CORRECT_MOVE
from constans.scenarios_shoot import (
    board_shoot_hole_player_1,
    board_shoot_hole_player_2,

)
from exceptions.personal_exceptions import invalidMoveException
from game.board import Board
from game.player import Player
from game.game import WumpusGame
from parameterized import parameterized
import unittest
from unittest.mock import MagicMock, patch


def patched_game() -> WumpusGame:
    with patch.object(Board, '_valid_hole', return_value=True):
        users_name = [NAME_USER_1, NAME_USER_2]
        game = WumpusGame(users_name)
    return game


class TestShootActions(unittest.TestCase):

    # shoot to hole
    @parameterized.expand([  # shoot to hole
        (board_shoot_hole_player_1(), Player(PLAYER_1, NAME_USER_1), 7, 10, NORTH, CORRECT_MOVE),
        (board_shoot_hole_player_1(), Player(PLAYER_1, NAME_USER_1), 15, 14, SOUTH, CORRECT_MOVE),
        (board_shoot_hole_player_2(), Player(PLAYER_2, NAME_USER_2), 5, 6, EAST, CORRECT_MOVE),
        (board_shoot_hole_player_2(), Player(PLAYER_2, NAME_USER_2), 13, 2, WEST, CORRECT_MOVE)
    ])
    def test_shoot_into_hole_return(self, board, player, row, col, direction, expected):
        game = patched_game()
        game._board._board = board
        current_player = player
        shoot_arrow = ShootArrow()
        shoot_to_hole = ShootToHole()
        shoot_arrow.set_next(shoot_to_hole)
        result = shoot_arrow.execute(row, col, direction, current_player, game._board)
        self.assertEqual(result, expected)

    # shoot to hole
    @parameterized.expand([  # shoot to hole
        (board_shoot_hole_player_1(), Player(PLAYER_1, NAME_USER_1), 7, 10, NORTH),
        (board_shoot_hole_player_1(), Player(PLAYER_1, NAME_USER_1), 15, 14, SOUTH),
        (board_shoot_hole_player_2(), Player(PLAYER_2, NAME_USER_2), 5, 6, EAST),
        (board_shoot_hole_player_2(), Player(PLAYER_2, NAME_USER_2), 13, 2, WEST)
    ])
    def test_shoot_into_hole_arrow_decrease(self, board, player, row, col, direction):
        game = patched_game()
        game._board._board = board
        current_player = player
        shoot_arrow = ShootArrow()
        shoot_to_hole = ShootToHole()
        shoot_arrow.set_next(shoot_to_hole)
        shoot_arrow.execute(row, col, direction, current_player, game._board)
        self.assertEqual(current_player.arrows, INITIAL_ARROWS - 1)

    # shoot to hole
    @parameterized.expand([  # shoot to hole
        (board_shoot_hole_player_1(), Player(PLAYER_1, NAME_USER_1), 7, 10, NORTH),
        (board_shoot_hole_player_1(), Player(PLAYER_1, NAME_USER_1), 15, 14, SOUTH),
    ])
    def test_shoot_into_hole_cell_discovered_P1(self, board, player, row, col, direction):
        game = patched_game()
        game._board._board = board
        current_player = player
        shoot_arrow = ShootArrow()
        shoot_to_hole = ShootToHole()
        shoot_arrow.set_next(shoot_to_hole)
        shoot_arrow.execute(row, col, direction, current_player, game._board)
        target_row, target_col = target_position_within_bounds(row, col, direction)
        target_cell = game._board.get_cell(target_row, target_col)
        self.assertTrue(target_cell.is_discover[0])

    # shoot to hole
    @parameterized.expand([  # shoot to hole
        (board_shoot_hole_player_2(), Player(PLAYER_2, NAME_USER_2), 5, 6, EAST),
        (board_shoot_hole_player_2(), Player(PLAYER_2, NAME_USER_2), 13, 2, WEST)
    ])
    def test_shoot_into_hole_cell_discovered_P2(self, board, player, row, col, direction):
        game = patched_game()
        game._board._board = board
        current_player = player
        shoot_arrow = ShootArrow()
        shoot_to_hole = ShootToHole()
        shoot_arrow.set_next(shoot_to_hole)
        shoot_arrow.execute(row, col, direction, current_player, game._board)
        target_row, target_col = target_position_within_bounds(row, col, direction)
        target_cell = game._board.get_cell(target_row, target_col)
        self.assertTrue(target_cell.is_discover[1])

    @parameterized.expand([  # shoot and kill parameterized
            (0, 0, EAST, Player(PLAYER_1, NAME_USER_1)),
            (8, 0, NORTH, Player(PLAYER_1, NAME_USER_1)),
            (0, 16, WEST, Player(PLAYER_2, NAME_USER_2)),
            (8, 16, SOUTH, Player(PLAYER_2, NAME_USER_2))
    ])
    def test_shoot_to_hole_get_next_action_called(self, row, col, direction, player):
        game = patched_game()
        current_player = player
        shoot_arrow = ShootArrow()
        shoot_to_hole = ShootToHole()
        shoot_to_hole.set_next(shoot_arrow)
        shoot_to_hole.get_next_action = MagicMock()
        shoot_to_hole.execute(row, col, direction, current_player, game._board)
        shoot_to_hole.get_next_action.assert_called()

    @parameterized.expand(
        [
            (0, 0, EAST, Player(PLAYER_1, NAME_USER_1)),
            (8, 0, NORTH, Player(PLAYER_1, NAME_USER_1)),
            (0, 16, WEST, Player(PLAYER_2, NAME_USER_2)),
            (8, 16, SOUTH, Player(PLAYER_2, NAME_USER_2))
        ])
    def test_shoot_to_hole_no_availabe_shoots_exeception(self, row, col, direction, player):
        game = patched_game()
        game.current_player = player
        shoot_to_hole = ShootToHole()
        with self.assertRaises(invalidMoveException):
            shoot_to_hole.execute(row, col, direction, game.current_player, game._board)
