from copy import deepcopy
import unittest
from unittest.mock import MagicMock, patch

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
    DICT_FILTER_MOVE_MK,
    DICTIONARY_ENE,
    DICTIONARY_H,
    DICTIONARY_MAK_MOV,
    DICTIONARY_MAK_MOV_P2,
    FILTER_MOVE_BOARD_ENE,
    filter_move_board_h,
    filter_move_make_move,
    FIN_FILTER_MOVE_BOARD_ENE,
    fin_filter_move_board_h,
    fin_filter_move_make_move,
    FIND_GOLD_POS_1,
    FIND_GOLD_POS_2,
    FIND_GOLD_POS_3,
    FIND_GOLD_POS_4,
    INITIAL_BIG_FAIL_BOARD,
    make_move_board,
    make_move_board_p2,
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
    moveToYourOwnCharPositionException,
    noArrowsAvailableException,
    noPossibleMoveException,
    notYourCharacterException,
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

    @parameterized.expand([  # case for filter event
        (DICTIONARY_H, filter_move_board_h(),
         fin_filter_move_board_h(), [
            Gold(), Gold(), Gold(), Gold(), Gold(), Diamond()
            ], 5, 1),
        (DICTIONARY_ENE, FILTER_MOVE_BOARD_ENE,
         FIN_FILTER_MOVE_BOARD_ENE, [
            Gold(), Gold(), Gold(), Gold(), Gold(), Diamond()
            ], 5, 1),
        (DICT_FILTER_MOVE_MK, filter_move_make_move(),
         fin_filter_move_make_move(), [], 0, 0)
    ])
    def test_filter_move(self, dictionary, initial_board,
                         finalboard, treasure, count_gold, count_diam):
        board = Board()
        board._board = initial_board
        board.filter_move(dictionary)
        cell = finalboard[dictionary["from_row"]][dictionary["from_col"]]
        cell.treasures = treasure
        gold_cel = cell.gold
        diam_cel = cell.diamond
        diam_char = cell.character
        self.assertEqual(gold_cel, count_gold)
        self.assertEqual(diam_cel, count_diam)
        self.assertIsNone(diam_char)

    @parameterized.expand([  # verify new cell is discovered
         (DICTIONARY_MAK_MOV, make_move_board(),
          True, False),
    ])
    def test_make_move_P1_new_cell_is_discovered(
        self, dictionary,
        initial_board,
        is_visited_p1,
        is_visited_p2,
    ):
        board = Board()
        board._board = initial_board
        board.make_move(dictionary)
        new_cell: Cell = board._board[
            dictionary["to_row"]][dictionary["to_col"]]
        self.assertEqual(new_cell.is_discover[0], is_visited_p1)
        self.assertEqual(new_cell.is_discover[1], is_visited_p2)

    @parameterized.expand([  # verify new cell objects
         (DICTIONARY_MAK_MOV, make_move_board(), 0, 0, 0),
    ])
    def test_make_move_P1_new_cell_objects(
        self, dictionary,
        initial_board,
        gold_old,
        diamond_old,
        old_arrow
    ):
        board = Board()
        board._board = initial_board
        board.make_move(dictionary)

        new_cell: Cell = board._board[
            dictionary["to_row"]][dictionary["to_col"]]
        self.assertEqual(new_cell.arrow, old_arrow)
        self.assertEqual(new_cell.gold, gold_old)
        self.assertEqual(new_cell.diamond, diamond_old)

    @parameterized.expand([  # verify old cell objects
         (DICTIONARY_MAK_MOV, make_move_board(),
          0, 0, 0),
    ])
    def test_make_move_P1_old_cell_objects(
        self, dictionary,
        initial_board,
        gold_old,
        diamond_old,
        old_arrow
    ):
        board = Board()
        board._board = initial_board
        board.make_move(dictionary)
        old_cell: Cell = board._board[
            dictionary["from_row"]][dictionary["from_col"]]
        self.assertEqual(old_cell.arrow, old_arrow)
        self.assertEqual(old_cell.gold, gold_old)
        self.assertEqual(old_cell.diamond, diamond_old)

    @parameterized.expand([  # verify player 1 objects
         (DICTIONARY_MAK_MOV, make_move_board(),
          3, 0, 2),
    ])
    def test_make_move_P1_player_objects(
        self, dictionary,
        initial_board,
        gold_new,
        diamond_new,
        new_arrows,
    ):
        board = Board()
        board._board = initial_board
        board.make_move(dictionary)
        player_character: Character = board.\
            _board[dictionary["to_row"]][dictionary["to_col"]].character
        self.assertIsNotNone(player_character)
        self.assertEqual(player_character.gold, gold_new)
        self.assertEqual(player_character.diamond, diamond_new)
        self.assertEqual(player_character.player.arrows, new_arrows)

    @parameterized.expand([  # verify new cell is discovered
         (DICTIONARY_MAK_MOV_P2, make_move_board_p2(), False, True)
    ])
    def test_make_move_P2_new_cell_is_discoverd(
        self,
        dictionary,
        initial_board,
        is_visited_p1,
        is_visited_p2,
    ):
        board = Board()
        board._board = initial_board
        board.make_move(dictionary)

        new_cell: Cell = board._board[
            dictionary["to_row"]][dictionary["to_col"]]

        self.assertEqual(new_cell.is_discover[0], is_visited_p1)
        self.assertEqual(new_cell.is_discover[1], is_visited_p2)

    @parameterized.expand([  # verify new cell objects
         (DICTIONARY_MAK_MOV_P2, make_move_board_p2(), 0, 0, 0)
    ])
    def test_make_move_P2_new_cell_objects(
        self,
        dictionary,
        initial_board,
        gold_old,
        diamond_old,
        old_arrow
    ):
        board = Board()
        board._board = initial_board
        board.make_move(dictionary)

        new_cell: Cell = board._board[
            dictionary["to_row"]][dictionary["to_col"]]
        self.assertEqual(new_cell.arrow, old_arrow)
        self.assertEqual(new_cell.gold, gold_old)
        self.assertEqual(new_cell.diamond, diamond_old)

    @parameterized.expand([  # verify old cell objects
         (DICTIONARY_MAK_MOV_P2, make_move_board_p2(), 0, 0, 0)
    ])
    def test_make_move_P2_old_cell_objects(
        self,
        dictionary,
        initial_board,
        gold_old,
        diamond_old,
        old_arrow
    ):
        board = Board()
        board._board = initial_board
        board.make_move(dictionary)
        old_cell: Cell = board._board[
            dictionary["from_row"]][dictionary["from_col"]]
        self.assertEqual(old_cell.arrow, old_arrow)
        self.assertEqual(old_cell.gold, gold_old)
        self.assertEqual(old_cell.diamond, diamond_old)

    @parameterized.expand([  # verify Player 2 objects
         (DICTIONARY_MAK_MOV_P2, make_move_board_p2(),
          5, 1, 3)
    ])
    def test_make_move_P2_player_objects(
        self,
        dictionary,
        initial_board,
        gold_new,
        diamond_new,
        new_arrows,
    ):
        board = Board()
        board._board = initial_board
        board.make_move(dictionary)
        player_character: Character = board.\
            _board[dictionary["to_row"]][dictionary["to_col"]].character

        self.assertIsNotNone(player_character)
        self.assertEqual(player_character.gold, gold_new)
        self.assertEqual(player_character.diamond, diamond_new)
        self.assertEqual(player_character.player.arrows, new_arrows)

    @parameterized.expand([  # verify string returned for Player 1
         (DICTIONARY_MAK_MOV, make_move_board(), CORRECT_MOVE)
    ])
    def test_make_move_P1_string_returned(
        self,
        dictionary,
        initial_board,
        expected_result,
    ):
        board = Board()
        board._board = initial_board
        result = board.make_move(dictionary)
        self.assertEqual(result, expected_result)

    @parameterized.expand([  # verify string returned for Player 2
         (DICTIONARY_MAK_MOV_P2, make_move_board_p2(), CORRECT_MOVE)
    ])
    def test_make_move_P2_string_returned(
        self,
        dictionary,
        initial_board,
        expected_result,
    ):
        board = Board()
        board._board = initial_board
        result = board.make_move(dictionary)
        self.assertEqual(result, expected_result)

    @parameterized.expand([
        (PLAYER_1, PLAYER_2, 0, 0, 0, 1)
    ])
    def test_is_valid_move_not_your_character(self, p1, p2,
                                              from_row, from_col,
                                              to_row, to_col):
        board = Board()
        player_1 = Player(p1)
        player_2 = Player(p2)
        character_1_of_player_1 = player_1.characters[0]
        board._board[from_row][from_col].character = character_1_of_player_1
        # try to move a character that is not yours, current player is Player 2
        # and try to move characters from player 1
        with self.assertRaises(notYourCharacterException):
            board.is_valid_move(
                from_row,
                from_col,
                to_row,
                to_col,
                player_2)

    @parameterized.expand([
        (PLAYER_1, 0, 0, -1, 0),
        (PLAYER_1, 0, 0, 3, 0),
        (PLAYER_1, 0, 0, 0, 0),
    ])
    def test_is_valid_move_not_possible_move(self, p1,
                                             from_row, from_col,
                                             to_row, to_col):
        board = Board()
        player_1 = Player(p1)
        character_1_of_player_1 = player_1.characters[0]
        board._board[from_row][from_col].character = character_1_of_player_1
        with self.assertRaises(noPossibleMoveException):
            board.is_valid_move(
                from_row,
                from_col,
                to_row,
                to_col,
                player_1)

    @parameterized.expand([
        (PLAYER_1, 0, 0, 0, 1),
    ])
    def test_is_valid_move_to_a_same_character(self, P1, from_row, from_col,
                                               to_row, to_col):
        board = Board()
        player_1 = Player(P1)
        character_1_of_player_1 = player_1.characters[0]
        character_2_of_player_1 = player_1.characters[1]
        board._board[from_row][from_col].character = character_1_of_player_1
        board._board[to_row][to_col].character = character_2_of_player_1
        with self.assertRaises(moveToYourOwnCharPositionException):
            board.is_valid_move(
                from_row,
                from_col,
                to_row,
                to_col,
                player_1
            )

    @parameterized.expand([
        (PLAYER_1, 0, 0, PLAYER_2, 0, 1, 0, 1, {
                'from_row': 0,
                'from_col': 0,
                'to_row': 0,
                'to_col': 1,
            }),
    ])
    def test_is_valid_move_good_move(self, P1, c1_row, c1_col, P2, c2_row,
                                     c2_col, to_row, to_col, _expected_result):
        expected_result = _expected_result
        board = Board()
        player_1 = Player(P1)
        player_2 = Player(P2)
        character_1_of_player_1 = player_1.characters[0]
        character_1_of_player_2 = player_2.characters[0]
        board._board[c1_row][c1_col].character = character_1_of_player_1
        board._board[c2_row][c2_col].character = character_1_of_player_2
        expected_result['player'] = player_1
        board.filter_move = MagicMock()
        board.is_valid_move(
            c1_row,
            c1_col,
            to_row,
            to_col,
            player_1)
        board.filter_move.assert_called_once()
        board.filter_move.assert_called_once_with(expected_result)

    def test_initial_diamond_position(self, row_random=4, expected_result=1):
        game = patched_game()
        mid_col = LARGE//2
        with patch('random.randint', return_value=row_random):
            game.initial_diamond_position()
        self.assertEqual(
            game._board[row_random][mid_col]
            .diamond, expected_result
        )


if __name__ == "__main__":
    unittest.main()
