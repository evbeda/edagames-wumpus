from copy import deepcopy
from constans.constans import (
    INITIAL_POSITION_PLAYER_1,
    INITIAL_POSITION_PLAYER_2,
    PLAYER_1,
    PLAYER_2,
)
from constans.constants_game import (
    GOLD,
    GOLD_QUANTITY,
    HOLE,
    HOLE_QUANTITY,
    MIDDLE,
    LARGE,
)
from constans.scenarios import (
    CLOSED_GOLD_BOARD,
    FIND_GOLD_POS_1,
    FIND_GOLD_POS_2,
    FIND_GOLD_POS_3,
    FIND_GOLD_POS_4,
    INITIAL_BIG_FAIL_BOARD,
    RECURSIVE,
    RECURSIVE_SIDE,
    RECURSIVE_SIDE_CORNER,
    VALID_HOLE_SCENARIO,
    WAY_GOLD_TWO_PLAYERS,
)
from game.board import Board
from game.cell import Cell
from game.player import Player
from parameterized import parameterized
from unittest.mock import patch
import unittest


def patched_game() -> Board:
    with patch.object(Board, '_valid_hole', return_value=True):
        board = Board()
    return board


class TestBoard(unittest.TestCase):

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

    def test_place_gold(self):
        board = patched_game()
        board._board = [
            [Cell(row, col) for col in range(LARGE)] for row in range(LARGE)
        ]
        board.place_items(GOLD, GOLD_QUANTITY)

        gold_quantity = sum([cell.gold
                            for row_cell in board._board
                            for cell in row_cell])

        golds_first_half = sum([board._board[row][col].gold
                                for col in range(MIDDLE)
                                for row in range(LARGE)])
        golds_second_half = sum([board._board[row][col].gold
                                for col in range(MIDDLE + 1, LARGE)
                                for row in range(LARGE)])

        self.assertEqual(gold_quantity, 16)
        self.assertEqual(golds_first_half, 8)
        self.assertEqual(golds_second_half, 8)

    def test_place_gold_position(self):
        gold_places = [
            (1, 1), (5, 0), (11, 0), (14, 4), (11, 5),
            (10, 7), (5, 5), (1, 3), (15, 15), (15, 12),
            (10, 12), (7, 11), (4, 9), (0, 15), (1, 12),
            (6, 9)]
        gold_places_patch = sum(gold_places, ())
        board = patched_game()
        with patch('random.randint', side_effect=list(gold_places_patch)):
            board._board = [
                [Cell(row, col)for col in range(LARGE)]
                for row in range(LARGE)
            ]
            board.place_items(GOLD, GOLD_QUANTITY)
            golds = [
                (row, col)
                for row, row_cell in enumerate(board._board)
                for col, cell in enumerate(row_cell)
                if cell.gold > 0]
            self.assertEqual(sorted(gold_places), sorted(golds))

    def test_place_holes(self):
        holes_positions = [
            (0, 3), (1, 2), (3, 4),
            (7, 6), (10, 3), (12, 1),
            (14, 1), (15, 11), (1, 13),
            (4, 13), (7, 15), (9, 12),
            (13, 15), (14, 9), (15, 15),
            (3, 14)]

        hole_places_patch = sum(holes_positions, ())
        board = patched_game()
        with patch('random.randint', side_effect=list(hole_places_patch)):
            board._board = [
                [Cell(row, col) for col in range(LARGE)]
                for row in range(LARGE)
            ]
            board.place_items(HOLE, HOLE_QUANTITY)
            holes = [
                position for position in holes_positions if (
                    board._board[position[0]][position[1]].has_hole is True
                    )
            ]
            self.assertEqual(sorted(holes_positions), sorted(holes))

    def test_holes_quantity(self):
        board = patched_game()
        board._board = [
            [Cell(row, col) for col in range(LARGE)] for row in range(LARGE)
        ]
        board.place_items(HOLE, HOLE_QUANTITY)

        hole_quantity = sum([cell.has_hole
                            for row_cell in board._board
                            for cell in row_cell])

        holes_first_half = sum([board._board[row][col].has_hole
                                for col in range(MIDDLE)
                                for row in range(LARGE)])
        holes_second_half = sum([board._board[row][col].has_hole
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
    def test_can_find_gold(
        self,
        char_position,
        gold_position,
        test_board,
        expected
    ):
        board = patched_game()
        board._board = deepcopy(test_board)
        row, col = char_position
        result = board._can_find_gold(row, col, gold_position, [])
        self.assertEqual(result, expected)

    @parameterized.expand([
        (FIND_GOLD_POS_1, [
                            (5, 7), (2, 7), (1, 7), (7, 4),
                            (7, 1), (3, 6), (2, 9), (10, 7),
                            (9, 7), ]),

        (FIND_GOLD_POS_2, [(4, 2), (2, 5), (3, 7), (7, 4), ]),
        (FIND_GOLD_POS_3, [(4, 2), ]),
        (FIND_GOLD_POS_4, []),
    ])
    def test_gold_positions(self, board, expected):
        game = patched_game()
        game._board = deepcopy(board)
        self.assertEqual(sorted(game._gold_positions()), sorted(expected))

    @parameterized.expand([
        (7, 10, True),
        (7, 4, False),
        (7, 5, False),
        (7, 3, False),
        (2, 0, False),
        (1, 0, False),
        (3, 0, False),
        (4, 0, True),
        (15, 0, False),
        (16, 1, False),
    ])
    def test_valid_hole(self, row, col, expected):
        board = patched_game()
        board._board = deepcopy(VALID_HOLE_SCENARIO)
        self.assertEqual(board._valid_hole(row, col), expected)
