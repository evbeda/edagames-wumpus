from copy import deepcopy
import unittest
from unittest.mock import patch
from parameterized import parameterized
from game.diamond import Diamond
from game.board import Board
from game.game import WumpusGame
from constans.constans import (
    EMPTY_CELL,
    PLAYER_1,
    PLAYER_2,
    INITIAL_ARROWS,
    INITIAL_SCORE,
    INVALID_MOVES_SCORE,
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
    TEST_PLAYERS_CHARACTER_0,
    TEST_PLAYERS_CHARACTER_1,
    TEST_PLAYERS_CHARACTER_2,
    SCENARIO_STR_PLAYER_1,
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
        game = WumpusGame()
        cell = Cell(2, 4)
        cell.treasures.append(Gold())
        cell.treasures.append(Gold())
        cell.treasures.append(Gold())
        cell.treasures.append(Diamond())
        payload = {"cell": cell}
        game.modify_score(GET_ITEMS, payload)
        self.assertEqual(game.current_player.score,
                         (SCORES[GOLD]*3 + SCORES[DIAMOND]*1))

    def test_modify_score_death(self):  # testing "Death" event
        game = WumpusGame()
        char = Character(Player(PLAYER_2))
        game.current_player = char.player
        char.treasures.append(Gold())
        char.treasures.append(Gold())
        char.treasures.append(Gold())
        char.treasures.append(Gold())
        payload = {"character": char}
        game.modify_score(DEATH, payload)
        self.assertEqual(char.player.score, (SCORES[GOLD]*4) * -1)

    @parameterized.expand([  # test for modify_score() function
        ("KILL", SCORES[KILL]),
        ("CORRECT_MOVE", SCORES[CORRECT_MOVE]),
        ("INVALID_MOVE", SCORES[INVALID_MOVE]),
        ("ARROW_MISS", SCORES[ARROW_MISS]),
        ("TIMEOUT", SCORES[TIMEOUT]),
    ])
    def test_modify_score(self, event, expected):

        game = WumpusGame()
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
        game = WumpusGame()
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
        game = WumpusGame()
        game.current_player = game.player_1
        game.player_1.name = "B"
        game.player_2.name = "P"
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
        game = WumpusGame()
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
        game = WumpusGame()
        self.assertIsInstance(game._board, Board)


if __name__ == '__main__':
    unittest.main()
