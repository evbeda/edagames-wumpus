import unittest
from game.game import WumpusGame
from constans.constants_game import LARGE
from game.cell import Cell


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
