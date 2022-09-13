import unittest
from parameterized import parameterized
from constans.constants_utils import (
    EAST,
    MOVE,
    SHOOT,
    NORTH,
    WEST,
    SOUTH
)
from game.character import Character
from game.game import WumpusGame
from game.player import Player
from constans.constans import (
    PLAYER_1,
    PLAYER_2,
    INITIAL_ARROWS,
    INITIAL_SCORE,
)
from constans.constants_game import LARGE
from game.cell import Cell


class TestPlayer(unittest.TestCase):

    @parameterized.expand([
        (PLAYER_1, INITIAL_ARROWS, INITIAL_SCORE),
        (PLAYER_2, INITIAL_ARROWS, INITIAL_SCORE),
    ])
    def test_player_init(self, name, expected_arrows, expected_score):
        self.player = Player(name)
        self.assertEqual(self.player.arrows, expected_arrows)
        self.assertEqual(self.player.score, expected_score)
        self.assertEqual(self.player.name, name)

    @parameterized.expand([
        (PLAYER_1, 0, -10000, -10000),
        (PLAYER_2, 5000, 10000, 15000),
    ])
    def test_update_score(self, player_name,
                          actual_score, score_mod, expected_result):
        self.player = Player(player_name)
        self.player.score = actual_score
        self.player.update_score(score_mod)
        self.assertEqual(self.player.score, expected_result)

    @parameterized.expand([
        (PLAYER_1, 4, -1, 3),
        (PLAYER_2, 0, 1, 1),
    ])
    def test_update_arrows(self, player_name,
                           actual_arrows, arrows_mod, expected_result):
        self.player = Player(player_name)
        self.player.arrows = actual_arrows
        self.player.update_arrows(arrows_mod)
        self.assertEqual(self.player.arrows, expected_result)

    @parameterized.expand([
        (MOVE, 0, 0, WEST, -100, 1),
        (SHOOT, 16, 0, SOUTH, -100, 1),
        (SHOOT, 0, 0, NORTH, -100, 1)
    ])
    def test_invalid_moves_count_player_1(
            self,
            action,
            from_row,
            from_col,
            direction,
            expected_score,
            expected_count
    ):

        game = WumpusGame()
        game._board = [
            [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)
        ]
        player = game.current_player
        game.place_character_initial_pos(
            player,
            Character(player),
            Character(player),
            Character(player)
            )
        game.action_manager(action, from_row, from_col, direction)
        score_result = game.current_player.score
        invalid_moves_count = game.current_player.invalid_moves_count
        self.assertEqual(score_result, expected_score)
        self.assertEqual(invalid_moves_count, expected_count)

    @parameterized.expand([
        (MOVE, 0, 16, EAST, -100, 1),
        (SHOOT, 16, 16, EAST, -100, 1),
        (SHOOT, 16, 16, SOUTH, -100, 1)
    ])
    def test_invalid_moves_count_player_2(
            self,
            action,
            from_row,
            from_col,
            direction,
            expected_score,
            expected_count
    ):

        game = WumpusGame()
        game._board = [
            [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)
        ]
        game.current_player = game.player_2
        player = game.current_player
        game.place_character_initial_pos(
            player,
            Character(player),
            Character(player),
            Character(player)
            )
        game.action_manager(action, from_row, from_col, direction)
        score_result = game.current_player.score
        invalid_moves_count = game.current_player.invalid_moves_count
        self.assertEqual(score_result, expected_score)
        self.assertEqual(invalid_moves_count, expected_count)

    @parameterized.expand([
        (MOVE, 0, 0, EAST, 100, 0),
        (MOVE, 16, 0, NORTH, 100, 0),
        (SHOOT, 8, 0, EAST, 100, 0)
    ])
    def test_valid_move_score_player_1(
            self,
            action,
            from_row,
            from_col,
            direction,
            expected_score,
            expected_count
    ):
        game = WumpusGame()
        game._board = [
            [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)
        ]
        player = game.current_player
        game.place_character_initial_pos(
            player,
            Character(player),
            Character(player),
            Character(player)
            )
        game.action_manager(action, from_row, from_col, direction)
        score_result = game.current_player.score
        invalid_moves_count = game.current_player.invalid_moves_count
        self.assertEqual(score_result, expected_score)
        self.assertEqual(invalid_moves_count, expected_count)


if __name__ == '__main__':
    unittest.main()
