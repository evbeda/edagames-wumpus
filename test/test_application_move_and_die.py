from application.move_and_die import MoveAndDie
from application.move import Move
from constans.constans import SOUTH, NORTH, WEST
from constans.constants_scores import CORRECT_MOVE
from parameterized import parameterized
from game.board import Board
from game.cell import Cell
from constans.scenarios import generate_board_for_move_action_test
from game.gold import Gold
from game.diamond import Diamond
from exceptions.personal_exceptions import invalidMoveException
from unittest.mock import patch
import unittest


class TestMoveAndDie(unittest.TestCase):

    def setUp(self):
        self.scenarios, self.moving_player, self.opponent_player = generate_board_for_move_action_test()
        self.move_n_die = MoveAndDie()
        self.board = Board()

    @parameterized.expand([
        (4, 4, NORTH, CORRECT_MOVE),
    ])
    def test_execute_move_and_die_return_correct_move(self, row, col, direction, expected_result):
        self.board._board = self.scenarios
        result = self.move_n_die.execute(row, col, direction, self.moving_player, self.board)
        self.assertEqual(result, expected_result)
        self.assertEqual(self.board._board[row][col].character, None)

    @parameterized.expand([
        (4, 4, NORTH, 0, 0, [Gold()], 1, 0),
        (4, 4, NORTH, 0, 0, [Diamond()], 0, 1),
        (4, 4, NORTH, 0, 0, [Gold(), Diamond(), Gold(), Diamond()], 2, 2),
    ])
    def test_execute_move_and_die_transfer_treasure(
        self,
        row,
        col,
        direction,
        expected_init_gold,
        expected_init_diamond,
        treasure_to_add_to_the_character,
        expected_final_gold,
        expected_final_diamond,
    ):
        self.board._board = self.scenarios
        cell: Cell = self.board.get_cell(row, col)

        # before the character dies treasures in cell
        self.assertEqual(cell.gold, expected_init_gold)
        self.assertEqual(cell.diamond, expected_init_diamond)

        cell.character.treasures.extend(treasure_to_add_to_the_character)
        self.move_n_die.execute(row, col, direction, self.moving_player, self.board)

        # after the character dies treasures in cell
        self.assertEqual(cell.gold, expected_final_gold)
        self.assertEqual(cell.diamond, expected_final_diamond)

    @parameterized.expand([
        (4, 4, NORTH, None),
        (8, 8, SOUTH, None),
    ])
    def test_execute_move_die_and_remove_the_character(
        self,
        row,
        col,
        direction,
        expected_character_in_origin_cell
    ):
        self.board._board = self.scenarios
        cell: Cell = self.board.get_cell(row, col)
        self.move_n_die.execute(row, col, direction, self.moving_player, self.board)
        self.assertEqual(cell.character, expected_character_in_origin_cell)

    @parameterized.expand([
        (4, 4, NORTH, 3, 4, True),
        (8, 8, SOUTH, 9, 8, True),
    ])
    def test_execute_move_die_and_discover_the_cell(
        self,
        row,
        col,
        direction,
        to_row,
        to_col,
        discover_final_status,
    ):
        self.board._board = self.scenarios
        cell: Cell = self.board.get_cell(to_row, to_col)
        self.move_n_die.execute(row, col, direction, self.moving_player, self.board)
        self.assertEqual(cell.is_discover[0], discover_final_status)

    @parameterized.expand([
        (4, 4, SOUTH, invalidMoveException)
    ])
    def test_execute_invalid_move_and_die_raise_exception(
        self,
        row,
        col,
        direction,
        exception_raised,
    ):
        self.board._board = self.scenarios
        with self.assertRaises(exception_raised):
            self.move_n_die.execute(
                row,
                col,
                direction,
                self.moving_player,
                self.board
                )

    @parameterized.expand([
        ('NEXT_ACTION', 'get_next_action', 4, 4, WEST)
    ])
    def test_execute_valid_move_to_hole_continue_the_chain_of_responsability(
        self,
        name_of_the_test_case,
        get_next_action_pathced,
        row,
        col,
        direction,

    ):
        move = Move()
        self.move_n_die.set_next(move)
        self.board._board = self.scenarios
        with patch.object(MoveAndDie, get_next_action_pathced) as patched_method:
            self.move_n_die.execute(
                row,
                col,
                direction,
                self.moving_player,
                self.board
                )
        patched_method.assert_called()
