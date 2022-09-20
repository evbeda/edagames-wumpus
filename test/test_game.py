from copy import deepcopy
import unittest
from unittest.mock import patch
from parameterized import parameterized
from game.diamond import Diamond
from game.board import Board
from game.game import WumpusGame
from constans.constans import (
    EAST,
    EMPTY_CELL,
    MOVE,
    NORTH,
    PLAYER_1,
    PLAYER_2,
    INITIAL_ARROWS,
    INITIAL_SCORE,
    INVALID_MOVES_SCORE,
    SHOOT,
    SOUTH,
    WEST,
)
from constans.constants_game import (
    DIAMOND,
    GOLD,
)
from game.cell import Cell
from game.character import Character
from game.gold import Gold
from game.player import Player
from constans.constants_scores import (
    ARROW_MISS,
    CORRECT_MOVE,
    DEATH,
    GET_ITEMS,
    INVALID_MOVE,
    KILL,
    SCORES,
    TIMEOUT,
)
from constans.scenarios import (
    BOARD_FOR_MOVE_AND_MODIFY_SCORE,
    DANGER_SIGNAL_SCENARIO,
    SCENARIOS_SHOOT_TEST,
    SHOOTER_PLAYER,
    TEST_PLAYERS_CHARACTER_0,
    TEST_PLAYERS_CHARACTER_1,
    TEST_PLAYERS_CHARACTER_2,
    SCENARIO_STR_PLAYER_1,
    board_player_1_scenario,
    generate_board_for_move_action_test,
)
from game.utils import posibles_positions


def patched_game() -> WumpusGame:
    with patch.object(Board, '_valid_hole', return_value=True):
        game = WumpusGame()
    return game


class TestGame(unittest.TestCase):

    def test_create_game(self):
        # check game attributes creation
        game = patched_game()
        self.assertIsNotNone(game._board)
        self.assertIsNotNone(game._board._board[0][0])
        self.assertIsInstance(game._board._board[0][0], Cell)
        self.assertEqual(game.player_1.name, PLAYER_1)
        self.assertEqual(game.player_2.name, PLAYER_2)
        self.assertTrue(game)

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

    def test_current_player(self):
        game = patched_game()
        self.assertEqual(game.current_player, game.player_1)

    def test_change_current_player(self):
        game = patched_game()
        game.change_current_player()
        self.assertEqual(game.current_player, game.player_2)

    def test_modify_score_get_items(self):  # testing "Get_Items" event
        game = patched_game()
        cell = Cell(2, 4)
        cell.treasures.append(Gold())
        cell.treasures.append(Gold())
        cell.treasures.append(Gold())
        cell.treasures.append(Diamond())
        payload = {"cell": cell}
        game.modify_score(GET_ITEMS, payload)
        self.assertEqual(game.current_player.score,
                         (SCORES[GOLD] * 3 + SCORES[DIAMOND] * 1))

    def test_modify_score_death(self):  # testing "Death" event
        game = patched_game()
        char = Character(Player(PLAYER_2))
        game.current_player = char.player
        char.treasures.append(Gold())
        char.treasures.append(Gold())
        char.treasures.append(Gold())
        char.treasures.append(Gold())
        payload = {"character": char}
        game.modify_score(DEATH, payload)
        self.assertEqual(char.player.score, (SCORES[GOLD] * 4) * -1)

    @parameterized.expand([  # test for modify_score() function
        ("KILL", SCORES[KILL] + SCORES[CORRECT_MOVE]),
        ("CORRECT_MOVE", SCORES[CORRECT_MOVE]),
        ("INVALID_MOVE", SCORES[INVALID_MOVE]),
        ("ARROW_MISS", SCORES[ARROW_MISS]),
        ("TIMEOUT", SCORES[TIMEOUT]),
    ])
    def test_modify_score(self, event, expected):

        game = patched_game()
        game.modify_score(event)
        self.assertEqual(game.current_player.score, expected)

    @parameterized.expand([(PLAYER_1, 4, 3, EMPTY_CELL, '~    ', ),
                           (PLAYER_1, 4, 5, EMPTY_CELL, '~    ', ),
                           (PLAYER_1, 5, 4, EMPTY_CELL, '~    ', ),
                           (PLAYER_1, 9, 9, EMPTY_CELL, EMPTY_CELL, ),
                           (PLAYER_1, 2, 2, EMPTY_CELL, EMPTY_CELL, ),
                           (PLAYER_1, 2, 3, EMPTY_CELL, '    +', ),
                           (PLAYER_1, 2, 5, EMPTY_CELL, '    +', ),
                           (PLAYER_1, 1, 4, EMPTY_CELL, '    +', ),
                           (PLAYER_1, 3, 4, EMPTY_CELL, '~   +', ),
                           (PLAYER_1, 2, 4, EMPTY_CELL, EMPTY_CELL, ),
                           (PLAYER_2, 7, 0, EMPTY_CELL, EMPTY_CELL, ),
                           (PLAYER_2, 7, 1, EMPTY_CELL, '    +', ),
                           (PLAYER_2, 7, 3, EMPTY_CELL, '    +', ),
                           (PLAYER_2, 6, 2, EMPTY_CELL, '    +', ),
                           (PLAYER_2, 8, 2, EMPTY_CELL, '    +', ),
                           ])
    def test_danger_signals(self, current_player, row, col,
                            parsed_cell, expected):

        game = patched_game()
        game._board._board = deepcopy(DANGER_SIGNAL_SCENARIO)
        game._board._board[2][2].character = Character(game.player_1)
        game._board._board[2][3].character = Character(game.player_1)
        game._board._board[2][4].character = Character(game.player_2)
        game._board._board[7][0].character = Character(game.player_2)
        game._board._board[7][1].character = Character(game.player_2)
        game._board._board[7][2].character = Character(game.player_1)

        if PLAYER_1 == current_player:
            game.current_player = game.player_1
        else:
            game.current_player = game.player_2
        result = game.put_danger_signal(parsed_cell, row, col)
        self.assertEqual(result, expected)

    def test_char_str(self):
        char = Character(Player(PLAYER_1))
        expected = f"gold: 0, player: {char.player}, diamonds: 0."
        self.assertEqual(str(char), expected)

    def test_make_move_and_modify_score(self):
        game = patched_game()
        game._board._board = BOARD_FOR_MOVE_AND_MODIFY_SCORE

        character = Character(game.player_1)
        game.player_1.characters.append(character)
        game._board._board[4][5].character = character
        dict_move = {
            "from_col": 5,
            "from_row": 4,
            "to_col": 5,
            "to_row": 5,
            "player": game.current_player
        }
        gold_before_move = character.gold
        diamonds_before_move = character.diamond

        result = game._board.make_move(dict_move)

        golds_after_move = character.gold
        diamonds_after_move = character.diamond
        self.assertEqual(gold_before_move, 0)
        self.assertEqual(diamonds_before_move, 0)
        self.assertEqual(golds_after_move, 2)
        self.assertEqual(diamonds_after_move, 1)
        self.assertEqual(CORRECT_MOVE, result)

    def test_generate_response(self):
        game = patched_game()
        game._board._board = board_player_1_scenario()
        game.current_player = game.player_1
        self.maxDiff = None
        expected_response = {
            "board": SCENARIO_STR_PLAYER_1,
            # "game_status": "active", # Add property when ready
            # "turn": "0" # Add property when ready
            "player1": {
                "name": PLAYER_1,
                "score": INITIAL_SCORE,
                "arrows": INITIAL_ARROWS,
                "characters_alive": 3,
            },
            "player2": {
                "name": PLAYER_2,
                "score": INITIAL_SCORE,
                "arrows": INITIAL_ARROWS,
                "characters_alive": 3,
            }
        }
        self.assertEqual(game.generate_response(), expected_response)

    @parameterized.expand([
        (10000, 8000, {
            'GAME_OVER': {
                'SCORE': {
                    PLAYER_1: 10000,
                    PLAYER_2: 8000,
                },
                'RESULT': {
                    'WINNER': PLAYER_1,
                    'LOSER': PLAYER_2,
                }
            }
        }),
        (8000, 10000, {
            'GAME_OVER': {
                'SCORE': {
                    PLAYER_1: 8000,
                    PLAYER_2: 10000,
                },
                'RESULT': {
                    'WINNER': PLAYER_2,
                    'LOSER': PLAYER_1,
                }
            }
        }),
        (10000, 10000, {
            'GAME_OVER': {
                'SCORE': {
                    PLAYER_1: 10000,
                    PLAYER_2: 10000,
                },
                'RESULT': 'DRAW',
            },
        }),
    ])
    def test_game_over_final_message(
        self,
        score_p1,
        score_p2,
        expected_result
    ):
        game = patched_game()
        game.player_1._score = score_p1
        game.player_2._score = score_p2
        result = game.game_over_final_message()
        self.assertEqual(result, expected_result)

    @parameterized.expand([
        (TEST_PLAYERS_CHARACTER_0, 5, INVALID_MOVES_SCORE, False),
        (TEST_PLAYERS_CHARACTER_0, 4, 80_000, True),
        (TEST_PLAYERS_CHARACTER_1, 5, INVALID_MOVES_SCORE, False),
        (TEST_PLAYERS_CHARACTER_1, 2, 130_000, True),
        (TEST_PLAYERS_CHARACTER_2, 5, INVALID_MOVES_SCORE, False),
        (TEST_PLAYERS_CHARACTER_2, 2, 1_000, True),
    ])
    def test_penalization_after_invalid_moves(
        self, current_player: Player, invalid_moves: int,
        expected_score: int, game_active: bool
    ):
        game = patched_game()
        game.current_player = deepcopy(current_player)
        game.current_player.invalid_moves_count = invalid_moves
        game.check_the_limit_of_invalid()
        self.assertEqual(game.current_player.score, expected_score)
        self.assertEqual(game.game_is_active, game_active)

    def test_board_game_is_class(self):
        game = patched_game()
        self.assertIsInstance(game._board, Board)

    @parameterized.expand([
        ('shoot opponent', 5, 8, 8, WEST, 8, 7, 16100, 4, "     "),
        ('shoot empty cell', 5, 8, 8, EAST, 8, 9, 1100, 4, "##F##"),
        ('shoot hole', 5, 8, 8, NORTH, 7, 8, 1100, 4, "  O  "),
        ('shoot own char', 5, 8, 8, SOUTH, 9, 8, 900, 4, "  B  "),
    ])
    def test_execute_action_shoot(self, name,
                                  initial_arrows,
                                  from_row, from_col, direction,
                                  destination_row, destination_col,
                                  expected_score, expected_arrows, expected_destination_cell):
        game = patched_game()

        game.player_1 = SHOOTER_PLAYER
        game.current_player = game.player_1

        game._board._board = deepcopy(SCENARIOS_SHOOT_TEST)
        game.current_player.score = 1000
        game.current_player.arrows = initial_arrows

        game.execute_action(SHOOT, from_row, from_col, direction)

        current_score = game.current_player.score
        current_arrows = game.current_player.arrows
        destination_cell = game._board._board[destination_row][destination_col]

        self.assertEqual(current_score, expected_score)
        self.assertEqual(current_arrows, expected_arrows)
        self.assertEqual(destination_cell.to_str(PLAYER_1), expected_destination_cell)

    @parameterized.expand([
        ('cell with hole', 4, 4, WEST, 1000, 4, 3, 1100, 2, EMPTY_CELL, '  O  '),
        ('cell empty', 4, 4, EAST, 1000, 4, 5, 1100, 3, EMPTY_CELL, '  B  '),
        ('cell with opponent char', 4, 4, NORTH, 1000, 3, 4, 1100, 2, EMPTY_CELL, '  P  '),
        ('cell with own char', 4, 4, SOUTH, 1000, 5, 4, 900, 3, '  B  ', '  B  '),
    ])
    def test_execute_action_move(self, name,
                                 from_row, from_col, direction, initial_socre,
                                 destination_row, destination_col,
                                 expected_score, expected_remaining_characters,
                                 expected_initial_cell, expected_destination_cell, ):
        game = patched_game()
        board, player_1, player_2 = generate_board_for_move_action_test()
        game.player_1 = player_1
        game.player_2 = player_2
        game.current_player = game.player_1
        game._board._board = board
        game.current_player.score = initial_socre

        game.execute_action(MOVE, from_row, from_col, direction)

        current_score = game.current_player.score
        initial_cell = game._board._board[from_row][from_col]
        destination_cell = game._board._board[destination_row][destination_col]
        current_remaining_characters = len(game.current_player.characters)

        self.assertEqual(current_score, expected_score)
        self.assertEqual(initial_cell.to_str(PLAYER_1), expected_initial_cell)
        self.assertEqual(destination_cell.to_str(PLAYER_1), expected_destination_cell)
        self.assertEqual(current_remaining_characters, expected_remaining_characters)

    @parameterized.expand([
        (PLAYER_1, 10, PLAYER_2, 9),
        (PLAYER_1, 200, PLAYER_2, 199),
        (PLAYER_2, 10, PLAYER_1, 9),
        (PLAYER_2, 15, PLAYER_1, 14),
    ])
    def test_next_turn(self, initial_player, initial_remaining_moves,
                       expected_player, expected_remainig_moves):

        game = patched_game()

        if PLAYER_1 == initial_player:
            game.current_player = game.player_1
        else:
            game.current_player = game.player_2

        game.remaining_moves = initial_remaining_moves

        game.next_turn()

        actual_player = game.current_player
        actual_remaining_moves = game.remaining_moves

        self.assertEqual(actual_player.name, expected_player)
        self.assertEqual(actual_remaining_moves, expected_remainig_moves)


if __name__ == '__main__':
    unittest.main()
