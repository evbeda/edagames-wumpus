from copy import deepcopy
import unittest
from unittest.mock import patch
from parameterized import parameterized

from game.game import WumpusGame
from constans.constans import PLAYER_1, PLAYER_2
from constans.constants_game import (
    GOLD_QUANTITY,
    HOLE,
    HOLE_QUANTITY,
    LARGE,
    MIDDLE,
    GOLD
)
from game.cell import Cell
from game.character import Character
from game.player import Player

from constans.scenarios import (
    BOARD_WITH_ITEMS,
    BOARD_WIOUT_ITEMS,
    CLOSED_GOLD_BOARD,
    INITIAL_BIG_FAIL_BOARD,
    RECURSIVE,
    RECURSIVE_SIDE,
    RECURSIVE_SIDE_CORNER,
    WAY_GOLD_TWO_PLAYERS
)
from game.utils import posibles_positions


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
        game._board = [
                [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)
            ]
        game.place_items(GOLD, GOLD_QUANTITY)

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

        game = WumpusGame()
        with patch('random.randint', side_effect=list(gold_places_patch)):
            game._board = [
                [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)
            ]
            game.place_items(GOLD, GOLD_QUANTITY)
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

    @parameterized.expand([  # there are two scenarios:
        # player with items, player without items
        (BOARD_WITH_ITEMS, 5, 5, 5, 1),
        (BOARD_WIOUT_ITEMS, 5, 5, 0, 0)
    ])
    def test_drop_items(self, board, row, col, golds, diamonds):
        game = WumpusGame()
        game._board = board
        game.drop_items(row, col)
        cel_board = game._board[row][col]
        self.assertEqual(cel_board.gold, golds)
        self.assertEqual(cel_board.diamond, diamonds)
        self.assertIsNone(cel_board.character)

    @parameterized.expand([

        (0, 0, [(0, 1), (1, 0)]),
        (16, 0, [(15, 0), (16, 1)]),
        (0, 16, [(0, 15), (1, 16)]),
        (16, 16, [(15, 16), (16, 15)]),
        (8, 0, [(7, 0), (9, 0), (8, 1)]),
        (0, 8, [(0, 7), (0, 9), (1, 8)]),
        (16, 8, [(16, 7), (16, 9), (15, 8)]),
        (8, 8, [(7, 8), (9, 8), (8, 7), (8, 9)]),

    ])
    def test_posibles_position(self, row, col, expected):

        positions = posibles_positions(row, col)
        self.assertEqual(sorted(positions), sorted(expected))

    def test_place_holes(self):
        holes_positions = [
            (0, 3), (1, 2), (3, 4),
            (7, 6), (10, 3), (12, 1),
            (14, 1), (15, 11), (1, 13),
            (4, 13), (7, 15), (9, 12),
            (13, 15), (14, 9), (15, 15),
            (3, 14)]

        hole_places_patch = sum(holes_positions, ())
        game = WumpusGame()
        with patch('random.randint', side_effect=list(hole_places_patch)):
            game._board = [
                [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)
            ]
            game.place_items(HOLE, HOLE_QUANTITY)
            holes = [
                position for position in holes_positions if (
                    game._board[position[0]][position[1]].has_hole > 0
                    )
            ]
            self.assertEqual(sorted(holes_positions), sorted(holes))

    def test_holes_quantity(self):
        game = WumpusGame()
        game._board = [
                [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)
            ]
        game.place_items(HOLE, HOLE_QUANTITY)

        hole_quantity = sum([cell.has_hole
                            for row_cell in game._board
                            for cell in row_cell])

        holes_first_half = sum([game._board[row][col].has_hole
                                for col in range(MIDDLE)
                                for row in range(LARGE)])
        holes_second_half = sum([game._board[row][col].has_hole
                                for col in range(MIDDLE + 1, LARGE)
                                for row in range(LARGE)])
        self.assertEqual(hole_quantity, HOLE_QUANTITY)
        self.assertEqual(holes_first_half, HOLE_QUANTITY // 2)
        self.assertEqual(holes_second_half, HOLE_QUANTITY // 2)

    @parameterized.expand([
        ((0, 0), (0, 1), RECURSIVE, True),
        ((0, 0), (4, 4), CLOSED_GOLD_BOARD, False),
        ((0, 0), (7, 7), INITIAL_BIG_FAIL_BOARD, False),
        ((0, 0), (2, 16), RECURSIVE_SIDE, False),
        ((0, 0), (16, 0), RECURSIVE_SIDE_CORNER, False),
        ((16, 0), (7, 7), WAY_GOLD_TWO_PLAYERS, False),
        ((0, 0), (7, 7), WAY_GOLD_TWO_PLAYERS, True),
        ((16, 16), (7, 7), WAY_GOLD_TWO_PLAYERS, True),
        ((16, 16), (16, 0), WAY_GOLD_TWO_PLAYERS, False),
    ])
    def test_can_find_gold(self, char_position, gold_position,
                           board, expected):
        game = WumpusGame()
        game._board = deepcopy(board)
        row, col = char_position
        result = game._can_find_gold(row, col, gold_position, board, [])
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
