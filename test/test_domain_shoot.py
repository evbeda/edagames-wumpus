import unittest
from constans.constans import (
    EAST,
    INITIAL_ARROWS,
    INITIAL_POSITION_PLAYER_1,
    NAME_USER_1,
    NAME_USER_2,
    NORTH,
    PLAYER_1,
    PLAYER_2,
    SOUTH,
    WEST,
)
from constans.constants_scores import ARROW_MISS, CORRECT_MOVE, KILL
from constans.scenarios import (
    board_empty_cell,
    board_friendly_fire_player_1,
    board_friendly_fire_player_2,
    board_kill_opp_player,
    board_shoot_hole_player_1,
    board_shoot_hole_player_2,
    shoot_arrow_board,
)
from domain.shoot_arrow import ShootArrow
from domain.shoot_and_kill import ShootAndKill
from domain.shoot_empty_cell import ShootEmptyCell
from domain.shoot_to_hole import ShootToHole
from domain.utils import target_position_within_bounds
from game.board import Board
from game.character import Character
from game.player import Player
from game.game import WumpusGame
from exceptions.personal_exceptions import friendlyFireException
from parameterized import parameterized
from unittest.mock import patch


def patched_game() -> WumpusGame:
    with patch.object(Board, '_valid_hole', return_value=True):
        users_name = [NAME_USER_1, NAME_USER_2]
        game = WumpusGame(users_name)
    return game


class TestShootActions(unittest.TestCase):

    @parameterized.expand([
        (board_friendly_fire_player_1(), Player(PLAYER_1, NAME_USER_1), 0, 0, EAST),
        (board_friendly_fire_player_2(), Player(PLAYER_2, NAME_USER_2), 0, 16, WEST),
    ])
    def test_shoot_own_character(self, board, player, row, col, direction):
        game = patched_game()
        game._board._board = board
        current_player = player
        shoot_arrow = ShootArrow()
        shoot_and_kill = ShootAndKill()
        shoot_arrow.set_next(shoot_and_kill)
        with self.assertRaises(friendlyFireException):
            shoot_arrow.execute(row, col, direction, current_player, game._board)

    @parameterized.expand([
        (board_kill_opp_player(), Player(PLAYER_1, NAME_USER_1), 0, 15, EAST, KILL),
        (board_kill_opp_player(), Player(PLAYER_2, NAME_USER_2), 8, 15, WEST, KILL)
    ])
    def test_kill_opp_return(self, board, player, row, col, direction, expected):
        game = patched_game()
        game._board._board = board
        current_player = player
        shoot_arrow = ShootArrow()
        shoot_and_kill = ShootAndKill()
        shoot_arrow.set_next(shoot_and_kill)
        result = shoot_arrow.execute(row, col, direction, current_player, game._board)
        self.assertEqual(result, expected)

    @parameterized.expand([
        (board_kill_opp_player(), Player(PLAYER_1, NAME_USER_1), 0, 15, EAST, 2),
        (board_kill_opp_player(), Player(PLAYER_2, NAME_USER_2), 8, 15, WEST, 3)
    ])
    def test_shoot_and_kill_treasures_transfer(self, board, player, row, col, direction, expected):
        game = patched_game()
        game._board._board = board
        current_player = player
        shoot_arrow = ShootArrow()
        shoot_and_kill = ShootAndKill()
        shoot_arrow.set_next(shoot_and_kill)
        shoot_arrow.execute(row, col, direction, current_player, game._board)
        target_row, target_col = target_position_within_bounds(row, col, direction)
        cell = game._board.get_cell(target_row, target_col)
        self.assertEqual(len(cell.treasures), expected)

    def test_kill_opp_remove_opp(self):
        game = patched_game()
        board = game._board
        current_player = Player(PLAYER_1, NAME_USER_1)
        board.place_character_initial_pos(
            current_player.characters,
            INITIAL_POSITION_PLAYER_1,
            0,
        )
        opp_player = Player(PLAYER_2, NAME_USER_2)
        opp_character = Character(opp_player)
        opp_player.characters = []
        opp_player.characters.append(opp_character)
        board._board[0][1].character = opp_character
        shoot_arrow = ShootArrow()
        shoot_and_kill = ShootAndKill()
        shoot_arrow.set_next(shoot_and_kill)
        shoot_arrow.execute(0, 0, EAST, current_player, board)
        self.assertEqual(board._board[0][1].character, None)

    def test_kill_opp_arrow_decrease(self):
        game = patched_game()
        board = game._board
        current_player = Player(PLAYER_1, NAME_USER_1)
        board.place_character_initial_pos(
            current_player.characters,
            INITIAL_POSITION_PLAYER_1,
            0,
        )
        opp_player = Player(PLAYER_2, NAME_USER_2)
        opp_character = Character(opp_player)
        opp_player.characters = []
        opp_player.characters.append(opp_character)
        board._board[0][1].character = opp_character
        shoot_arrow = ShootArrow()
        shoot_and_kill = ShootAndKill()
        shoot_arrow.set_next(shoot_and_kill)
        shoot_arrow.execute(0, 0, EAST, current_player, board)
        self.assertEqual(current_player.arrows, INITIAL_ARROWS - 1)

    @parameterized.expand([
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

    @parameterized.expand([
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

    @parameterized.expand([
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

    @parameterized.expand([
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

    @parameterized.expand([
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

    @parameterized.expand([
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

    @parameterized.expand([
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

    @parameterized.expand([
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

    @parameterized.expand([
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


if __name__ == "__main__":
    unittest.main()
