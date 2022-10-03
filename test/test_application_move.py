from application.move import Move
from application.move_and_die import MoveAndDie
from constants.constants import NORTH, SOUTH, WEST
from constants.scenarios import (
    generate_board_for_move_action_test,
)

from exceptions.personal_exceptions import (
    invalidMoveException,
    moveToYourOwnCharPositionException,
    notYourCharacterException,
    noPossibleMoveException,
)

from game.board import Board
from parameterized import parameterized
import unittest
from unittest.mock import patch


class TestMove(unittest.TestCase):

    def setUp(self):
        self.scenarios, self.moving_player, self.opponent_player = generate_board_for_move_action_test()
        self.move = Move()
        self.board = Board()

    @parameterized.expand([
        ('raise_invalid_move_exception', 4, 4, WEST, invalidMoveException),
        ('raise_move_to_your_own_char_exception', 4, 4, SOUTH, moveToYourOwnCharPositionException),
        ('raise_no_possible_move_exception', 0, 0, NORTH, noPossibleMoveException),
        ('raise_not_your_character_exeption_1', 9, 8, SOUTH, notYourCharacterException),
        ('raise_not_your_character_exeption_2', 3, 4, SOUTH, notYourCharacterException),
    ])
    def test_analize_the_correct_rising_exception_for_each_case_in_move(
        self,
        name_of_the_testcase,
        row,
        col,
        direction,
        exception_expected_to_raise,
    ):
        self.board._board = self.scenarios
        with self.assertRaises(exception_expected_to_raise):
            self.move.execute(
                row,
                col,
                direction,
                self.moving_player,
                self.board
                )

    @parameterized.expand([
        ('next_action_move_and_die', 'get_next_action', 4, 4, WEST)
    ])
    def test_execute_valid_move_continue__the_chain_of_responsability(
        self,
        name_of_the_test_case,
        get_next_action_pathced,
        row,
        col,
        direction,

    ):
        move_n_die = MoveAndDie()
        self.move.set_next(move_n_die)
        self.board._board = self.scenarios
        with patch.object(Move, get_next_action_pathced) as patched_method:
            self.move.execute(
                row,
                col,
                direction,
                self.moving_player,
                self.board
                )
        patched_method.assert_called()
