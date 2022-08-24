import unittest
from game.game import WumpusGame
from constans.constants_game import (LARGE)
from constans.constans import (PLAYER_1)
from game.cell import Cell
from game.character import Character


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
        cel_player = Cell()
        cel_character = Character(PLAYER_1)
        cel_player.character = cel_character
        game._board[5][5] = cel_player
        with self.assertRaises(Exception):
            game.move_to_own_character_position(PLAYER_1, 5, 5)
