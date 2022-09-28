from copy import deepcopy
import unittest
from parameterized import parameterized
from constans.scenarios import (
    TEST_PLAYERS_CHARACTER_0,
    TEST_PLAYERS_CHARACTER_1,
    TEST_PLAYERS_CHARACTER_2,
)
from game.player import Player
from constans.constans import (
    EAST,
    INITIAL_POSITION_PLAYER_1,
    INITIAL_POSITION_PLAYER_2,
    MOVE,
    NORTH,
    SOUTH,
    SHOOT,
    PLAYER_1,
    PLAYER_2,
    INITIAL_ARROWS,
    INITIAL_SCORE,
    WEST,
    NAME_USER_1,
)
from constans.constants_game import LARGE
from game.cell import Cell
from test.test_game import patched_game


class TestPlayer(unittest.TestCase):

    @parameterized.expand([
        (PLAYER_1, INITIAL_ARROWS, INITIAL_SCORE),
        (PLAYER_2, INITIAL_ARROWS, INITIAL_SCORE),
    ])
    def test_player_init(self, name, expected_arrows, expected_score):
        self.player = Player(name, NAME_USER_1)
        self.assertEqual(self.player.arrows, expected_arrows)
        self.assertEqual(self.player.score, expected_score)
        self.assertEqual(self.player.name, name)

    @parameterized.expand([
        (PLAYER_1, 0, -10000, -10000),
        (PLAYER_2, 5000, 10000, 15000),
    ])
    def test_update_score(self, player_name,
                          actual_score, score_mod, expected_result):
        self.player = Player(player_name, NAME_USER_1)
        self.player.score = actual_score
        self.player.update_score(score_mod)
        self.assertEqual(self.player.score, expected_result)

    @parameterized.expand([
        (PLAYER_1, 4, -1, 3),
        (PLAYER_2, 0, 1, 1),
    ])
    def test_update_arrows(self, player_name,
                           actual_arrows, arrows_mod, expected_result):
        self.player = Player(player_name, NAME_USER_1)
        self.player.arrows = actual_arrows
        self.player.update_arrows(arrows_mod)
        self.assertEqual(self.player.arrows, expected_result)

    @parameterized.expand([
        (MOVE, 0, 0, WEST, -1000, 1),
        (SHOOT, 16, 0, SOUTH, -1000, 1),
        (SHOOT, 0, 0, NORTH, -1000, 1)
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
        game = patched_game()
        game._board._board = [
            [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)
        ]
        game._board.place_character_initial_pos(game.player_1.characters,
                                                INITIAL_POSITION_PLAYER_1,
                                                0)
        game.execute_action(action, from_row, from_col, direction)
        score_result = game.current_player.score
        invalid_moves_count = game.current_player.invalid_moves_count
        self.assertEqual(score_result, expected_score)
        self.assertEqual(invalid_moves_count, expected_count)

    @parameterized.expand([
        (MOVE, 0, 16, EAST, -1000, 1),
        (SHOOT, 16, 16, EAST, -1000, 1),
        (SHOOT, 16, 16, SOUTH, -1000, 1)
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
        game = patched_game()
        game._board._board = [
            [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)
        ]
        game.current_player = game.player_2
        game._board.place_character_initial_pos(game.player_2.characters,
                                                INITIAL_POSITION_PLAYER_2,
                                                1)
        game.execute_action(action, from_row, from_col, direction)
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
        game = patched_game()
        game._board._board = [
            [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)
        ]
        game._board.place_character_initial_pos(game.player_1.characters,
                                                INITIAL_POSITION_PLAYER_1,
                                                0)
        game.execute_action(action, from_row, from_col, direction)
        score_result = game.current_player.score
        invalid_moves_count = game.current_player.invalid_moves_count
        self.assertEqual(score_result, expected_score)
        self.assertEqual(invalid_moves_count, expected_count)

    @parameterized.expand([
        (TEST_PLAYERS_CHARACTER_0,),
        (TEST_PLAYERS_CHARACTER_1,),
        (TEST_PLAYERS_CHARACTER_2,),
    ])
    def test_drop_caracters_treseaures(self, player: Player):
        player = deepcopy(player)
        player.drop_caracters_treseaures()
        characters_without_treseaures = all([not character.treasures
                                            for character in player.characters]
                                            )
        self.assertTrue(characters_without_treseaures)


if __name__ == '__main__':
    unittest.main()
