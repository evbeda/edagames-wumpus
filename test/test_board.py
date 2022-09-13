import unittest
from constans.constans import (
    INITIAL_POSITION_PLAYER_1,
    INITIAL_POSITION_PLAYER_2,
    PLAYER_1,
    PLAYER_2,
)
from game.board import Board
from game.player import Player

from constans.constants_game import LARGE


class TestGame(unittest.TestCase):

    def test_board_size(self):
        board = Board()
        self.assertEqual(len(board._board), LARGE)
        self.assertEqual(len(board._board[0]), LARGE)

    def test_place_character_initial_pos_player_1(self):
        board = Board()
        player_1 = Player(PLAYER_1)
        board.place_character_initial_pos(
            player_1.characters,
            INITIAL_POSITION_PLAYER_1,
            0)
        for index, character in enumerate(player_1.characters):
            row, col = INITIAL_POSITION_PLAYER_1[index]
            self.assertEqual(board._board[row][col].character, character)
            self.assertTrue(board._board[row][col].is_discover[0])

    def test_place_character_initial_pos_player_2(self):
        board = Board()
        player_2 = Player(PLAYER_2)
        board.place_character_initial_pos(
            player_2.characters,
            INITIAL_POSITION_PLAYER_2,
            1)
        for index, character in enumerate(player_2.characters):
            row, col = INITIAL_POSITION_PLAYER_2[index]
            self.assertEqual(board._board[row][col].character, character)
            self.assertTrue(board._board[row][col].is_discover[1])
