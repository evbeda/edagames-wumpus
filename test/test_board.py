from copy import deepcopy
import unittest
from unittest.mock import patch

from parameterized import parameterized

from constants.constants import (
    INITIAL_POSITION_PLAYER_1,
    INITIAL_POSITION_PLAYER_2,
    PLAYER_1,
    PLAYER_2,
    NAME_USER_1,
    NAME_USER_2,
    GOLD,
    GOLD_QUANTITY,
    HOLE,
    HOLE_QUANTITY,
    MIDDLE,
    LARGE,
)
from constants.scenarios import (
    CLOSED_GOLD_BOARD,
    DUPLICATE_FIRST_COOR_FOR_GOLDS_PLACEMENT,
    DUPLICATE_FIRST_COOR_FOR_HOLES_PLACEMENT,
    EMPTY_BOARD,
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
    LEFT_HALF_COORDS,
    RIGHT_HALF_COORDS,
)
from game.board import Board
from game.cell import Cell
from game.character import Character
from game.gold import Gold
from game.player import Player
from test.test_game import patched_game


def patched_board() -> Board:
    with patch.object(Board, '_valid_hole', return_value=True):
        board = Board()
    return board


class TestBoard(unittest.TestCase):

    def test_board_is_created_with_right_dimensions(self):
        board = patched_board()
        self.assertEqual(len(board._board), LARGE)
        self.assertEqual(len(board._board[0]), LARGE)

    @parameterized.expand(
        [
            (PLAYER_1, INITIAL_POSITION_PLAYER_1, 0, NAME_USER_1),
            (PLAYER_1, INITIAL_POSITION_PLAYER_1, 1, NAME_USER_1),
            (PLAYER_1, INITIAL_POSITION_PLAYER_1, 2, NAME_USER_1),
            (PLAYER_2, INITIAL_POSITION_PLAYER_2, 0, NAME_USER_2),
            (PLAYER_2, INITIAL_POSITION_PLAYER_2, 1, NAME_USER_2),
            (PLAYER_2, INITIAL_POSITION_PLAYER_2, 2, NAME_USER_2),
        ]
    )
    def test_place_character_initial_pos_player(
        self,
        player,
        init_positions,
        char_index,
        name_user,

    ):
        board = patched_board()
        current_player = Player(player, name_user)
        row, col = init_positions[char_index]
        board.place_character_initial_pos(
            current_player.characters,
            init_positions,
            0,
        )
        self.assertEqual(
            board._board[row][col].character,
            current_player.characters[char_index]
        )

    @parameterized.expand(
        [
            (PLAYER_1, 2, 2, 0, NAME_USER_1),
            (PLAYER_2, 5, 5, 1, NAME_USER_2),
        ]
    )
    def test_discover_cell_player(
        self,
        player_name,
        row,
        col,
        is_discover_pos,
        name_user
    ):
        board = patched_board()
        player = Player(player_name, name_user)
        board.discover_cell(row, col, player)
        result = board._board[row][col].is_discover[is_discover_pos]
        self.assertEqual(result, True)

    def test_place_gold(self):
        board = patched_board()
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
            (6, 9),
        ]
        #  gold_places_patch = sum(gold_places, ())
        board = patched_board()
        with patch('random.choice', side_effect=gold_places):
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
            (3, 14),
        ]
        board = patched_board()
        with patch('random.choice', side_effect=holes_positions):
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
        board = patched_board()
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
        game = patched_board()
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
    ])
    def test_valid_hole(self, row, col, expected):
        board = patched_board()
        board._board = deepcopy(VALID_HOLE_SCENARIO)
        self.assertEqual(board._valid_hole(row, col), expected)

    def test_initial_diamond_position(self, row_random=4, expected_result=1):
        board = Board()
        board._board = EMPTY_BOARD
        mid_col = LARGE//2
        with patch('random.randint', return_value=row_random):
            board.initial_diamond_position()
        self.assertEqual(
            board._board[row_random][mid_col]
            .diamond, expected_result
        )

    def test_only_right_HOLE_QUANTITY_have_to_be_placed(self):
        board = Board()
        board._board = []
        board._board = [
            [Cell(row, col) for col in range(LARGE)]
            for row in range(LARGE)
        ]
        board.place_items(GOLD, GOLD_QUANTITY)
        board.place_items(HOLE, HOLE_QUANTITY)
        self.assertEqual(board.item_quantity(HOLE), HOLE_QUANTITY)

    def test_hole_is_removed_if_is_no_valid_hole(self):
        board = Board()
        player = Player(PLAYER_1, NAME_USER_1)
        board._board = [
            [Cell(row, col) for col in range(LARGE)]
            for row in range(LARGE)
        ]
        board.place_character_initial_pos(
            player.characters,
            INITIAL_POSITION_PLAYER_1,
            0,
        )
        board._board[5][5].treasures.append(Gold())
        board._board[3][0].has_hole = True
        board._board[2][1].has_hole = True
        board._board[1][2].has_hole = True

        board._valid_hole(0, 3)

        self.assertFalse(board._board[0][3].has_hole)

    @parameterized.expand(
        [
            (
                "GOLD", GOLD, GOLD_QUANTITY, DUPLICATE_FIRST_COOR_FOR_GOLDS_PLACEMENT,
            ),
            (
                "HOLE", HOLE, HOLE_QUANTITY, DUPLICATE_FIRST_COOR_FOR_HOLES_PLACEMENT,
            ),
        ]
    )
    def test_correct_amount_of_items_should_be_placed_when_ranint_generate_duplicate_coor(
        self,
        name,
        item,
        item_quantity,
        item_coor,
    ):
        """
        It test only workes if length of the board is less than 16.
        In other cases the item_coor parameter must be modified
        """
        items_coor_patch = sum(item_coor, ())
        board = Board()
        board._board = [
            [Cell(row, col) for col in range(LARGE)] for row in range(LARGE)
        ]

        with patch('random.randint', side_effect=items_coor_patch):
            board.place_items(item, item_quantity)
        self.assertEqual(item_quantity, board.item_quantity(item))

    def test_initialize_free_cells(self):
        board = Board()
        board._free_cells = []
        board._free_cells_left_half = []
        board._free_cells_right_half = []
        board.initialize_free_cells()
        self.assertEqual(board._free_cells_left_half, LEFT_HALF_COORDS)
        self.assertEqual(board._free_cells_right_half, RIGHT_HALF_COORDS)

    @parameterized.expand([
        ('from (0, 0) to (3, 3)', 3, 3, [(1, 0), (0, 1), ], [(0, 1), (1, 0), ]),
        ('from (0, 1) to (3, 3)', 3, 3, [(0, 0), (0, 2), (1, 1), ], [(1, 1), (0, 2), (0, 0)]),
        ('from (1, 1) to (3, 3)', 3, 3, [(0, 1), (2, 1), (1, 0), (1, 2)], [(1, 2), (2, 1), (0, 1), (1, 0), ]),
        ('from (1, 2) to (3, 3)', 3, 3, [(0, 2), (2, 2), (1, 3), (1, 1)], [(2, 2), (1, 3), (1, 1), (0, 2), ]),
        ('from (2, 2) to (3, 3)', 3, 3, [(1, 2), (3, 2), (2, 3), (2, 1)], [(2, 3), (3, 2), (1, 2), (2, 1), ]),
        ('from (2, 3) to (3, 3)', 3, 3, [(1, 3), (3, 3), (2, 4), (2, 2)], [(3, 3), (2, 4), (2, 2), (1, 3), ]),

        ('from (0, 0) to (2, 0)', 2, 0, [(1, 0), (0, 1), ], [(1, 0), (0, 1), ]),
        ('from (1, 0) to (2, 0)', 2, 0, [(0, 0), (1, 1), (2, 0)], [(2, 0), (1, 1), (0, 0), ]),

    ])
    def test_sort_possibles_position(self, name,
                                     destination_row, destination_col,
                                     positions, expeted_sorted_possitions):
        board = patched_board()
        sorted_possitions = board.sort_possibles_position(positions,
                                                          destination_row, destination_col,)
        self.assertEqual(sorted_possitions, expeted_sorted_possitions)

    def test_has_opponent_player(self):
        game = patched_game()
        player_2 = Player(PLAYER_2, NAME_USER_2)
        character = Character(player_2)
        result = game._board.has_opponent_player(character, game.current_player)
        self.assertEqual(result, True)


if __name__ == "__main__":
    unittest.main()
