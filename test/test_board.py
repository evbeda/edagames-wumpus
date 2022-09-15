from copy import deepcopy
import unittest
from unittest.mock import patch

from parameterized import parameterized

from constans.constans import (
    INITIAL_ARROWS,
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
from constans.constants_scores import (
    ARROW_MISS,
    CORRECT_MOVE,
    KILL,
)
from constans.constants_utils import (
    NORTH,
    SOUTH,
    EAST,
    WEST,
)
from exceptions.personal_exceptions import (
    friendlyFireException,
    noArrowsAvailableException,
    shootOutOfBoundsException,
)
from game.character import Character
from game.diamond import Diamond
from game.gold import Gold
from game.player import Player


def patched_game() -> Board:
    with patch.object(Board, '_valid_hole', return_value=True):
        board = Board()
    return board


class TestBoard(unittest.TestCase):

    def test_board_is_created_with_right_dimensions(self):
        board = Board()
        self.assertEqual(len(board._board), LARGE)
        self.assertEqual(len(board._board[0]), LARGE)

    @parameterized.expand(
        [
            (PLAYER_1, INITIAL_POSITION_PLAYER_1, 0),
            (PLAYER_1, INITIAL_POSITION_PLAYER_1, 1),
            (PLAYER_1, INITIAL_POSITION_PLAYER_1, 2),
            (PLAYER_2, INITIAL_POSITION_PLAYER_2, 0),
            (PLAYER_2, INITIAL_POSITION_PLAYER_2, 1),
            (PLAYER_2, INITIAL_POSITION_PLAYER_2, 2),
        ]
    )
    def test_place_character_initial_pos_player(
        self,
        player,
        init_positions,
        char_index
    ):
        board = Board()
        current_player = Player(player)
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

    def test_no_arrows_availabe(self):
        current_player = Player(PLAYER_1)
        board = Board()
        current_player.arrows = 0
        with self.assertRaises(noArrowsAvailableException):
            board.there_are_arrows_available(current_player)

    def test_friendly_fire(self):
        board = Board()
        current_player = Player(PLAYER_1)
        row, col = INITIAL_POSITION_PLAYER_1[1]
        board.place_character_initial_pos(
            current_player.characters,
            INITIAL_POSITION_PLAYER_1,
            0
        )
        board._board[0][1].character = board._board[row][col].character
        board._board[row][col].character = None

        with self.assertRaises(friendlyFireException):
            board.is_not_frendly_fire(
                board._board[0][1],
                current_player,
            )

    @parameterized.expand(
        [
            (0, 0, NORTH),
            (0, 0, WEST),
            (16, 16, SOUTH),
            (16, 16, EAST)
        ]
    )
    def test_target_position_exception(self, row, col, direction):
        board = Board()
        with self.assertRaises(shootOutOfBoundsException):
            board.target_position(row, col, direction)

    @parameterized.expand(
        [
            (0, 0, SOUTH, (1, 0)),
            (0, 0, EAST, (0, 1)),
            (16, 16, NORTH, (15, 16)),
            (16, 16, WEST, (16, 15))
        ]
    )
    def test_target_position_ok(self, row, col, direction, expected):
        board = Board()
        result = board.target_position(row, col, direction)
        self.assertEqual(result, expected)

    def test_shoot_own_character(self):
        board = Board()
        current_player = Player(PLAYER_1)
        character = Character(current_player)
        board._board[0][1].character = character
        with self.assertRaises(friendlyFireException):
            board.shoot_arrow(0, 0, EAST, current_player)

    def test_kill_opp_return(self):
        board = Board()
        current_player = Player(PLAYER_1)
        board.place_character_initial_pos(
            current_player.characters,
            INITIAL_POSITION_PLAYER_1,
            0,
        )
        opp_player = Player(PLAYER_2)
        opp_character = Character(opp_player)
        board._board[0][1].character = opp_character
        result = board.kill_opp(0, 1, current_player)
        self.assertEqual(result, KILL)

    def test_shoot_and_kill_treasures_transfer(self):
        board = Board()
        current_player = Player(PLAYER_1)
        board.place_character_initial_pos(
            current_player.characters,
            INITIAL_POSITION_PLAYER_1,
            0,
        )
        opp_player = Player(PLAYER_2)
        opp_character = Character(opp_player)
        opp_character.treasures.append(Diamond())
        opp_character.treasures.append(Gold())
        opp_character.treasures.append(Gold())
        board._board[0][1].treasures = []
        board._board[0][1].character = opp_character
        board.kill_opp(0, 1, current_player)
        self.assertEqual(len(board._board[0][1].treasures), 3)

    def test_kill_opp_remove_opp(self):
        board = Board()
        current_player = Player(PLAYER_1)
        board.place_character_initial_pos(
            current_player.characters,
            INITIAL_POSITION_PLAYER_1,
            0,
        )
        opp_player = Player(PLAYER_2)
        opp_character = Character(opp_player)
        board._board[0][1].character = opp_character
        board.kill_opp(0, 1, current_player)
        self.assertEqual(board._board[0][1].character, None)

    def test_kill_opp_arrow_decrease(self):
        board = Board()
        current_player = Player(PLAYER_1)
        board.place_character_initial_pos(
            current_player.characters,
            INITIAL_POSITION_PLAYER_1,
            0,
        )
        opp_player = Player(PLAYER_2)
        opp_character = Character(opp_player)
        board._board[0][1].character = opp_character
        board.kill_opp(0, 1, current_player)
        self.assertEqual(current_player.arrows, INITIAL_ARROWS - 1)

    def test_shoot_into_hole_return(self):
        board = Board()
        current_player = Player(PLAYER_1)
        row = 0
        col = 1
        target_cell = board._board[row][col]
        target_cell.has_hole = True
        result = board.shoot_hole(row, col, current_player)
        self.assertEqual(result, CORRECT_MOVE)

    def test_shoot_into_hole_arrow_decrease(self):
        board = Board()
        current_player = Player(PLAYER_1)
        row = 0
        col = 1
        target_cell = board._board[row][col]
        target_cell.has_hole = True
        board.shoot_hole(row, col, current_player)
        self.assertEqual(current_player.arrows, INITIAL_ARROWS - 1)

    def test_shoot_into_hole_cell_discovered(self):
        board = Board()
        current_player = Player(PLAYER_1)
        row = 0
        col = 1
        target_cell = board._board[row][col]
        target_cell.has_hole = True
        board.shoot_hole(row, col, current_player)
        self.assertTrue(target_cell.is_discover[0])

    def test_shoot_miss_return(self):
        board = Board()
        current_player = Player(PLAYER_1)
        row = 0
        col = 1
        result = board.shoot_miss(row, col, current_player)
        self.assertEqual(result, ARROW_MISS)

    def test_shoot_miss_arrow_decrease(self):
        board = Board()
        current_player = Player(PLAYER_1)
        row = 0
        col = 1
        board.shoot_miss(row, col, current_player)
        self.assertEqual(current_player.arrows, INITIAL_ARROWS - 1)

    def test_shoot_miss_cell_discover(self):
        board = Board()
        current_player = Player(PLAYER_1)
        row = 0
        col = 1
        target_cell = board._board[row][col]
        board.shoot_miss(row, col, current_player)
        self.assertTrue(target_cell.is_discover[0])

    def test_shoot_miss_cell_arrow_increase(self):
        board = Board()
        current_player = Player(PLAYER_1)
        row = 0
        col = 1
        target_cell = board._board[row][col]
        board.shoot_miss(row, col, current_player)
        self.assertEqual(target_cell.arrow, 1)

    @parameterized.expand(
        [
            (0, 0, EAST, CORRECT_MOVE,),
            (0, 0, SOUTH, ARROW_MISS,),
            (16, 0, NORTH, KILL,),
        ]
    )
    def test_shoot_arrow(self, row, col, direction, expected):
        board = Board()
        current_player = Player(PLAYER_1)
        board.place_character_initial_pos(
            current_player.characters,
            INITIAL_POSITION_PLAYER_1,
            0,
        )
        opp_player = Player(PLAYER_2)
        board._board[row-1][col].character = opp_player.characters[0]
        board._board[0][1].has_hole = True
        result = board.shoot_arrow(row, col, direction, current_player)
        self.assertEqual(result, expected)

    @parameterized.expand(
        [
            (PLAYER_1, 2, 2, 0),
            (PLAYER_2, 5, 5, 1),
        ]
    )
    def test_discover_cell_player(
        self,
        player_name,
        row,
        col,
        is_discover_pos,
    ):
        board = Board()
        player = Player(player_name)
        board.discover_cell(row, col, player)
        result = board._board[row][col].is_discover[is_discover_pos]
        self.assertEqual(result, True)

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
