import unittest
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
from constans.constants_scores import ARROW_MISS, CORRECT_MOVE, KILL
from constans.scenarios_shoot import (
    board_empty_cell,
    board_kill_opp_player,
    board_shoot_hole_player_1,
    board_shoot_hole_player_2,
    shoot_arrow_board,
)
from application.shoot_arrow import ShootArrow
from application.shoot_and_kill import ShootAndKill
from application.shoot_to_empty_cell import ShootEmptyCell
from application.shoot_to_hole import ShootToHole
from application.utils import target_position_within_bounds
from game.board import Board
from game.player import Player
from game.game import WumpusGame
from exceptions.personal_exceptions import invalidMoveException
from parameterized import parameterized
from unittest.mock import MagicMock, patch


def patched_game() -> WumpusGame:
    with patch.object(Board, '_valid_hole', return_value=True):
        users_name = [NAME_USER_1, NAME_USER_2]
        game = WumpusGame(users_name)
    return game


class TestShootActions(unittest.TestCase):

    @parameterized.expand([  # shoot to empty cell
        (board_empty_cell(), Player(PLAYER_1, NAME_USER_1), 7, 10, NORTH),
        (board_empty_cell(), Player(PLAYER_1, NAME_USER_1), 7, 10, SOUTH),
    ])
    def test_shoot_empty_cell_return(self, board, player, row, col, direction):
        game = patched_game()
        game._board._board = board
        current_player = player
        shoot_arrow = ShootArrow()
        shoot_empty_cell = ShootEmptyCell()
        shoot_arrow.set_next(shoot_empty_cell)
        result = shoot_arrow.execute(row, col, direction, current_player, game._board)
        self.assertEqual(result, ARROW_MISS)

    @parameterized.expand([  # shoot to empty cell
        (board_empty_cell(), Player(PLAYER_1, NAME_USER_1), 7, 10, NORTH),
        (board_empty_cell(), Player(PLAYER_1, NAME_USER_1), 7, 10, SOUTH),
    ])
    def test_shoot_empty_cell_decrease(self, board, player, row, col, direction):
        game = patched_game()
        game._board._board = board
        current_player = player
        shoot_arrow = ShootArrow()
        shoot_empty_cell = ShootEmptyCell()
        shoot_arrow.set_next(shoot_empty_cell)
        shoot_arrow.execute(row, col, direction, current_player, game._board)
        self.assertEqual(current_player.arrows, INITIAL_ARROWS - 1)

    @parameterized.expand([  # shoot to empty cell
        (board_empty_cell(), Player(PLAYER_1, NAME_USER_1), 7, 10, NORTH),
        (board_empty_cell(), Player(PLAYER_1, NAME_USER_1), 7, 10, SOUTH),
    ])
    def test_shoot_empty_cell_not_discover(self, board, player, row, col, direction):
        game = patched_game()
        game._board._board = board
        current_player = player
        shoot_arrow = ShootArrow()
        shoot_empty_cell = ShootEmptyCell()
        shoot_arrow.set_next(shoot_empty_cell)
        shoot_arrow.execute(row, col, direction, current_player, game._board)
        target_row, target_col = target_position_within_bounds(row, col, direction)
        target_cell = game._board.get_cell(target_row, target_col)
        self.assertTrue(not target_cell.is_discover[0])

    @parameterized.expand([  # shoot to empty cell
        (board_empty_cell(), Player(PLAYER_1, NAME_USER_1), 7, 10, NORTH),
        (board_empty_cell(), Player(PLAYER_1, NAME_USER_1), 7, 10, SOUTH),
    ])
    def test_shoot_empty_cell_arrow_increase(self, board, player, row, col, direction):
        game = patched_game()
        game._board._board = board
        current_player = player
        shoot_arrow = ShootArrow()
        shoot_empty_cell = ShootEmptyCell()
        shoot_arrow.set_next(shoot_empty_cell)
        shoot_arrow.execute(row, col, direction, current_player, game._board)
        target_row, target_col = target_position_within_bounds(row, col, direction)
        target_cell = game._board.get_cell(target_row, target_col)
        self.assertEqual(target_cell.arrow, 1)

    @parameterized.expand([  # shoot to empty cell
        (shoot_arrow_board(), Player(PLAYER_1, NAME_USER_1), 0, 4, EAST, CORRECT_MOVE),
        (shoot_arrow_board(), Player(PLAYER_1, NAME_USER_1), 8, 10, SOUTH, ARROW_MISS),
        (shoot_arrow_board(), Player(PLAYER_2, NAME_USER_2), 15, 6, WEST, KILL),
    ])
    def test_shoot_arrow(self, board, player, row, col, direction, expected):
        game = patched_game()
        game._board._board = board
        current_player = player
        # initialize chain
        shoot_arrow = ShootArrow()
        shoot_and_kill = ShootAndKill()
        shoot_to_hole = ShootToHole()
        shoot_empty_cell = ShootEmptyCell()

        # assign chain of responsability
        shoot_arrow.set_next(shoot_and_kill)
        shoot_and_kill.set_next(shoot_to_hole)
        shoot_to_hole.set_next(shoot_empty_cell)

        result = shoot_arrow.execute(row, col, direction, current_player, game._board)
        self.assertEqual(result, expected)

    @parameterized.expand([  # shoot and kill parameterized
            (board_shoot_hole_player_1(), Player(PLAYER_1, NAME_USER_1), 7, 10, NORTH),
            (board_shoot_hole_player_2(), Player(PLAYER_2, NAME_USER_2), 13, 2, WEST)
    ])
    def test_shoot_empty_cell_get_next_action_called(self, board, player, row, col, direction):
        game = patched_game()
        current_player = player
        game._board._board = board
        shoot_to_empty_cell = ShootEmptyCell()
        shoot_to_hole = ShootToHole()
        shoot_to_empty_cell.set_next(shoot_to_hole)
        shoot_to_empty_cell.get_next_action = MagicMock()
        shoot_to_empty_cell.execute(row, col, direction, current_player, game._board)
        shoot_to_empty_cell.get_next_action.assert_called()

    @parameterized.expand(
        [
            (board_kill_opp_player(), Player(PLAYER_1, NAME_USER_1), 0, 15, EAST),
            (board_kill_opp_player(), Player(PLAYER_2, NAME_USER_2), 8, 15, WEST)
        ])
    def test_shoot_empty_cell_no_availabe_shoots_exeception(self, board, player, row, col, direction):
        game = patched_game()
        game._board._board = board
        game.current_player = player
        shoot_to_hole = ShootEmptyCell()
        with self.assertRaises(invalidMoveException):
            shoot_to_hole.execute(row, col, direction, game.current_player, game._board)


if __name__ == "__main__":
    unittest.main()
