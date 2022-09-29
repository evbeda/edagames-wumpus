from application.shoot_and_kill import ShootAndKill
from application.shoot_arrow import ShootArrow
from application.utils import target_position_within_bounds
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
from constans.scenarios_shoot import board_friendly_fire_player_1, board_friendly_fire_player_2, board_kill_opp_player
from constans.constants_scores import KILL
from exceptions.personal_exceptions import (
    friendlyFireException,
    invalidMoveException,
    noArrowsAvailableException,
    notYourCharacterException,
    shootOutOfBoundsException,
)
from game.board import Board
from game.character import Character
from game.game import WumpusGame
from game.player import Player
from parameterized import parameterized
import unittest
from unittest.mock import MagicMock, patch


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

    @parameterized.expand([  # shoot and kill parameterized
        (board_kill_opp_player(), Player(PLAYER_1, NAME_USER_1), 0, 15, EAST, KILL),
        (board_kill_opp_player(), Player(PLAYER_2, NAME_USER_2), 8, 15, WEST, KILL)
    ])
    def test_shoot_arrow_get_next_action_called(self, board, player, row, col, direction, expected):
        game = patched_game()
        game._board._board = board
        current_player = player
        shoot_arrow = ShootArrow()
        shoot_and_kill = ShootAndKill()
        shoot_arrow.set_next(shoot_and_kill)
        shoot_arrow.get_next_action = MagicMock()
        shoot_arrow.execute(row, col, direction, current_player, game._board)
        shoot_arrow.get_next_action.assert_called()

    @parameterized.expand(
        [
            (0, 0, EAST, Player(PLAYER_1, NAME_USER_1)),
            (8, 0, NORTH, Player(PLAYER_1, NAME_USER_1)),
            (0, 16, WEST, Player(PLAYER_2, NAME_USER_2)),
            (8, 16, SOUTH, Player(PLAYER_2, NAME_USER_2))
        ])
    def test_shoot_arrow_no_availabe_shoots_exeception(self, row, col, direction, player):
        game = patched_game()
        game.current_player = player
        shoot_arrow = ShootArrow()
        with self.assertRaises(invalidMoveException):
            shoot_arrow.execute(row, col, direction, game.current_player, game._board)

    @parameterized.expand([  # shoot and kill parameterized
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

    @parameterized.expand([  # shoot and kill parameterized
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

    # shoot and kill
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

    # shoot and kill
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

    @parameterized.expand([  # shoot and kill parameterized
            (0, 0, EAST, Player(PLAYER_1, NAME_USER_1)),
            (8, 0, NORTH, Player(PLAYER_1, NAME_USER_1)),
            (0, 16, WEST, Player(PLAYER_2, NAME_USER_2)),
            (8, 16, SOUTH, Player(PLAYER_2, NAME_USER_2))
    ])
    def test_shoot_and_kill_get_next_action_called(self, row, col, direction, player):
        game = patched_game()
        current_player = player
        shoot_arrow = ShootArrow()
        shoot_and_kill = ShootAndKill()
        shoot_and_kill.set_next(shoot_arrow)
        shoot_and_kill.get_next_action = MagicMock()
        shoot_and_kill.execute(row, col, direction, current_player, game._board)
        shoot_and_kill.get_next_action.assert_called()

    @parameterized.expand(
        [
            (0, 0, EAST, Player(PLAYER_1, NAME_USER_1)),
            (8, 0, NORTH, Player(PLAYER_1, NAME_USER_1)),
            (0, 16, WEST, Player(PLAYER_2, NAME_USER_2)),
            (8, 16, SOUTH, Player(PLAYER_2, NAME_USER_2))
        ])
    def test_shoot_and_kill_no_availabe_shoots_exeception(self, row, col, direction, player):
        game = patched_game()
        game.current_player = player
        shoot_and_kill = ShootAndKill()
        with self.assertRaises(invalidMoveException):
            shoot_and_kill.execute(row, col, direction, game.current_player, game._board)


if __name__ == '__main__':
    unittest.main()
