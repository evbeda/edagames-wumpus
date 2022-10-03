from application.move_to_empty import MoveToEmpty
from application.move import Move
from application.utils import target_position_within_bounds
from constants.constants import EAST, NORTH
from constants.scenarios import generate_board_for_move_action_test
from game.board import Board
from game.cell import Cell
from game.character import Character
from game.diamond import Diamond
from game.gold import Gold
from parameterized import parameterized
from exceptions.personal_exceptions import invalidMoveException
from unittest.mock import patch
import unittest


class TestMoveToEmpty(unittest.TestCase):

    def setUp(self):
        self.scenarios, self.moving_player, self.opponent_player = generate_board_for_move_action_test()
        self.move_to_empty = MoveToEmpty()
        self.board = Board()

    @parameterized.expand([
        (8, 8, NORTH, 6, 7),
        (4, 4, EAST, 6, 6),
    ])
    def test_move_to_empty_and_transfer_the_arrows_from_cell_to_player(
        self,
        row,
        col,
        direction,
        expected_player_init_arrows,
        expected_player_final_arrows,
    ):
        self.board._board = self.scenarios
        cell: Cell = self.board.get_cell(row, col)
        moving_character: Character = cell.character

        # initial arrows of the player
        self.assertEqual(
            moving_character.player.arrows, expected_player_init_arrows
            )
        self.move_to_empty.execute(row, col, direction, self.moving_player, self.board)

        # final arrows of the player
        self.assertEqual(
            moving_character.player.arrows, expected_player_final_arrows
        )

    @parameterized.expand([
        (4, 4, EAST, 4, 5, False, True, 0),
        (8, 8, NORTH, 7, 8, False, True, 0),
    ])
    def test_execute_move_to_empty_and_discover_the_cell(
        self,
        row,
        col,
        direction,
        to_row,
        to_col,
        discover_init_status,
        discover_final_status,
        player_index_in_discover_cell
    ):
        self.board._board = self.scenarios
        cell: Cell = self.board.get_cell(to_row, to_col)

        # forced to be undiscovered the target cell
        cell.is_discover[player_index_in_discover_cell] = discover_init_status

        self.move_to_empty.execute(row, col, direction, self.moving_player, self.board)
        self.assertEqual(cell.is_discover[player_index_in_discover_cell], discover_final_status)

    @parameterized.expand([
        (4, 4, EAST, 0, 0, [], 0, 0),
        (4, 4, EAST, 1, 0, [Gold()], 1, 0),
        (4, 4, EAST, 2, 2, [Gold(), Gold(), Diamond(), Diamond()], 2, 2),
        (8, 8, EAST, 2, 1, [], 3, 1),
        (8, 8, EAST, 2, 2, [Diamond()], 3, 2),
    ])
    def test_execute_move_to_empty_transfer_treasure_from_target_cell_to_character(
        self,
        row,
        col,
        direction,
        expected_init_gold_in_target_cell,
        expected_init_diamond_in_target_cell,
        treasure_to_add_to_the_cell,
        expected_final_gold_in_char,
        expected_final_diamond_in_char,
    ):
        self.board._board = self.scenarios
        to_row, to_col = target_position_within_bounds(row, col, direction)
        target_cell: Cell = self.board.get_cell(to_row, to_col)

        # add treasures if nescesary for the test
        target_cell.treasures.extend(treasure_to_add_to_the_cell)

        # verify the treasures in target cell
        self.assertEqual(target_cell.gold, expected_init_gold_in_target_cell)
        self.assertEqual(target_cell.diamond, expected_init_diamond_in_target_cell)

        self.move_to_empty.execute(row, col, direction, self.moving_player, self.board)

        # the treasures in target cell pass to character
        self.assertEqual(target_cell.character.gold, expected_final_gold_in_char)
        self.assertEqual(target_cell.character.diamond, expected_final_diamond_in_char)

    @parameterized.expand([
        (4, 4, EAST, None),

    ])
    def test_move_to_empty_and_remove_the_char_from_origin_cell_add_it_to_target_cell(
        self,
        row,
        col,
        direction,
        origin_cell_expected_char_value,
    ):
        self.board._board = self.scenarios
        origin_cell: Cell = self.board.get_cell(row, col)
        moving_character: Character = origin_cell.character
        to_row, to_col = target_position_within_bounds(row, col, direction)
        target_cell: Cell = self.board.get_cell(to_row, to_col)

        self.move_to_empty.execute(row, col, direction, self.moving_player, self.board)

        self.assertEqual(origin_cell.character, origin_cell_expected_char_value)
        self.assertEqual(target_cell.character, moving_character)

    @parameterized.expand([
        ('move_to_empty_to_next_action', 'get_next_action', 4, 4, NORTH)
    ])
    def test_execute_valid_move_is_not_move_to_hole_continue_the_chain_of_responsability(
        self,
        name_of_the_test_case,
        get_next_action_pathced,
        row,
        col,
        direction,
    ):
        move = Move()
        self.move_to_empty.set_next(move)
        self.board._board = self.scenarios
        with patch.object(MoveToEmpty, get_next_action_pathced) as patched_method:
            self.move_to_empty.execute(
                row,
                col,
                direction,
                self.moving_player,
                self.board
                )
        patched_method.assert_called()

    @parameterized.expand([
        (4, 4, NORTH, invalidMoveException)
    ])
    def test_execute_invalid_move_to_hole_raise_exception(
        self,
        row,
        col,
        direction,
        exception_raised,
    ):
        self.board._board = self.scenarios
        with self.assertRaises(exception_raised):
            self.move_to_empty.execute(
                row,
                col,
                direction,
                self.moving_player,
                self.board
                )
