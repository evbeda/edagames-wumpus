import unittest
from unittest.mock import patch
from parameterized import parameterized
from game.game import WumpusGame

from constans.constans import PLAYER_1, PLAYER_2
from constans.constants_game import LARGE, MIDDLE

from game.cell import Cell
from game.character import Character
from game.player import Player


class TestGame(unittest.TestCase):

    def test_create_game(self):
        # comprobe game attributes creation
        game = WumpusGame()
        self.assertIsNotNone(game._board)
        self.assertIsNotNone(game._board[0][0])
        self.assertIsInstance(game._board[0][0], Cell)
        self.assertEqual(game.player_1, None)
        self.assertEqual(game.player_2, None)
        self.assertTrue(game)

    def test_board_size(self):
        game = WumpusGame()
        self.assertEqual(len(game._board), LARGE)
        self.assertEqual(len(game._board[0]), LARGE)

    def test_move_player_to_other_player_position(self):
        game = WumpusGame()
        cel_player = Cell(0, 0)
        cel_character = Character(PLAYER_1)
        cel_player.character = cel_character
        game._board[5][5] = cel_player
        with self.assertRaises(Exception):
            game.move_to_own_character_position(PLAYER_1, 5, 5)

    def test_place_character_initial_pos_player_1(self):
        game = WumpusGame()
        player = Player(PLAYER_1)
        character1 = Character(player)
        character2 = Character(player)
        character3 = Character(player)
        game.place_character_initial_pos(
            player,
            character1,
            character2,
            character3
        )
        self.assertEqual(game._board[0][0].character, character1)
        self.assertEqual(game._board[8][0].character, character2)
        self.assertEqual(game._board[16][0].character, character3)

    def test_place_character_initial_pos_player_2(self):
        game = WumpusGame()
        player = Player(PLAYER_2)
        character1 = Character(player)
        character2 = Character(player)
        character3 = Character(player)
        game.place_character_initial_pos(
            player,
            character1,
            character2,
            character3
        )
        self.assertEqual(game._board[0][16].character, character1)
        self.assertEqual(game._board[8][16].character, character2)
        self.assertEqual(game._board[16][16].character, character3)

    def test_place_gold(self):

        game = WumpusGame()
        # game.place_golds()

        gold_quantity = sum([cell.gold
                            for row_cell in game._board
                            for cell in row_cell])

        golds_first_half = sum([game._board[row][col].gold
                                for col in range(MIDDLE)
                                for row in range(LARGE)])
        golds_second_half = sum([game._board[row][col].gold
                                for col in range(MIDDLE + 1, LARGE)
                                for row in range(LARGE)])

        self.assertEqual(gold_quantity, 16)
        self.assertEqual(golds_first_half, 8)
        self.assertEqual(golds_second_half, 8)

    def test_place_gold_position(self):

        gold_places = [(1, 1), (5, 0), (11, 0), (14, 4), (11, 5),
                       (10, 7), (5, 5), (1, 3), (16, 16), (15, 12),
                       (10, 12), (7, 11), (4, 9), (0, 16), (1, 12),
                       (6, 9)]
        gold_places_patch = sum(gold_places, ())

        with patch('random.randint', side_effect=list(gold_places_patch)):
            game = WumpusGame()
            golds = [
                (row, col)
                for row, row_cell in enumerate(game._board)
                for col, cell in enumerate(row_cell)
                if cell.gold > 0]
            self.assertEqual(sorted(gold_places), sorted(golds))

    @parameterized.expand([
        (4, 1)
    ])
    def test_initial_diamond_position(self, row_random, expected_result):
        game = WumpusGame()
        mid_col = LARGE//2
        with patch('random.randint', return_value=row_random):
            game.initial_diamond_position()
        self.assertEqual(game._board[row_random][mid_col].diamond,
                         expected_result)


if __name__ == '__main__':
    unittest.main()
