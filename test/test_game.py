from copy import deepcopy
import unittest
from unittest.mock import patch
from parameterized import parameterized
from application.initialize_chain_responsibility import initialize_chain_responsibility
from game.diamond import Diamond
from game.board import Board
from game.game import WumpusGame
from constans.constans import (
    EAST,
    EMPTY_CELL,
    MAXIMUM_INVALID_MOVES,
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
    NAME_USER_1,
    NAME_USER_2,
    DIAMOND,
    GOLD,
)
from game.cell import Cell
from game.character import Character
from game.gold import Gold
from game.player import Player
from constans.constans import (
    ARROW_MISS,
    CORRECT_MOVE,
    DEATH,
    GET_ITEMS,
    INVALID_MOVE,
    KILL,
    SCORES,
    TIMEOUT_SC,
)
from constans.constans import (
    GAME_OVER_MESSAGE_1,
    GAME_OVER_MESSAGE_2,
    GAME_OVER_MESSAGE_3,
    GAME_OVER_MESSAGE_4,
    GAME_OVER_MESSAGE_5,
    GAME_OVER_NOT_MET,
)
from constans.scenarios import (
    BOARD_FOR_MOVE_AND_MODIFY_SCORE,
    DANGER_SIGNAL_SCENARIO,
    TEST_PLAYERS_CHARACTER_0,
    TEST_PLAYERS_CHARACTER_1,
    TEST_PLAYERS_CHARACTER_2,
    SCENARIO_STR_PLAYER_1,
    generate_board_for_move_action_test,
    generate_board_for_shoot_action_test,
)
from game.utils import posibles_positions


def patched_game() -> WumpusGame:
    with patch.object(Board, '_valid_hole', return_value=True):
        users_name = [NAME_USER_1, NAME_USER_2]
        game = WumpusGame(users_name)
    return game


class TestGame(unittest.TestCase):

    def test_create_game(self):
        # check game attributes creation
        game = patched_game()
        self.assertIsNotNone(game._board)
        self.assertIsNotNone(game._board._board[0][0])
        self.assertIsInstance(game._board._board[0][0], Cell)
        self.assertEqual(game.player_1.side, PLAYER_1)
        self.assertEqual(game.player_2.side, PLAYER_2)
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
        char = Character(Player(PLAYER_2, NAME_USER_2))
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
        ("TIMEOUT", SCORES[TIMEOUT_SC]),
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
        char = Character(Player(PLAYER_1, NAME_USER_1))
        expected = f"gold: 0, player: {char.player}, diamonds: 0."
        self.assertEqual(str(char), expected)

    def test_make_move_and_modify_score(self):
        game = patched_game()
        game._board._board = BOARD_FOR_MOVE_AND_MODIFY_SCORE

        character = Character(game.player_1)
        game.player_1.characters.append(character)
        game._board._board[4][5].character = character
        from_col = 5
        from_row = 4
        direction = SOUTH
        player = game.current_player

        gold_before_move = character.gold
        diamonds_before_move = character.diamond
        action = initialize_chain_responsibility(MOVE)
        result = action.execute(from_row, from_col, direction, player, game._board)

        golds_after_move = character.gold
        diamonds_after_move = character.diamond
        self.assertEqual(gold_before_move, 0)
        self.assertEqual(diamonds_before_move, 0)
        self.assertEqual(golds_after_move, 2)
        self.assertEqual(diamonds_after_move, 1)
        self.assertEqual(CORRECT_MOVE, result)

    def test_generate_data(self):
        game = patched_game()
        game.current_player = game.player_1
        game_id = "1234-5678-9012-3456-7890"
        game.game_id = game_id
        self.maxDiff = None
        expected_response = {
            "player_2": NAME_USER_2,
            "player_1": NAME_USER_1,
            "score_1": 0,
            "score_2": 0,
            "arrows_1": INITIAL_ARROWS,
            "arrows_2": INITIAL_ARROWS,
            "board": SCENARIO_STR_PLAYER_1,
            "remaining_turns": 200,
            "game_id": game_id,
            "side": PLAYER_1,
        }
        self.assertEqual(game.generate_data(), expected_response)

    @parameterized.expand([
        (10000, 8000, Player(PLAYER_1, NAME_USER_1), Player(PLAYER_2, NAME_USER_2)),
        (8000, 10000, Player(PLAYER_1, NAME_USER_1), Player(PLAYER_2, NAME_USER_2)),
        (10000, 10000, Player(PLAYER_1, NAME_USER_1), Player(PLAYER_2, NAME_USER_2)),
    ])
    def test_game_over_final_message(
        self,
        score_p1,
        score_p2,
        player_1,
        player_2
    ):
        game = patched_game()
        game.player_1._score = score_p1
        game.player_2._score = score_p2

        expected = {
            "player_2": game.player_2.user_name,
            "player_1": game.player_1.user_name,
            "score_1": game.player_1.score,
            "score_2": game.player_2.score,
            "arrows_1": game.player_1.arrows,
            "arrows_2": game.player_2.arrows,
            "board": game.board,
            "remaining_turns": game.remaining_moves,
            "game_id": game.game_id,
            "side": game.current_player.side,
            "result": "DRAW" if score_p1 == score_p2 else {
                "WINNER": game.player_1.user_name if score_p2 < score_p1 else game.player_2.user_name,
                "LOSER": game.player_2.user_name if score_p2 < score_p1 else game.player_1.user_name
            }
        }
        result = game.game_over_final_message()
        self.assertEqual(result, expected)

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

    @parameterized.expand([  # test generate response
        ("p1", -100, 0, 50),
        (None, 0, 0, 200),
        ("p2", 0, -100, 30,),
        (None, 0, 0, 0),
        (None, 5000, 1000, 0),
        (None, 1000, 5000, 0),
    ])
    def test_generate_response(self, noChars, p1_score, p2_score, remining_moves):
        game = WumpusGame([NAME_USER_1, NAME_USER_2])
        self.maxDiff = None
        game_id = "1234-5678-9012-3456-7890"
        game.game_id = game_id
        game.player_1.score = p1_score
        game.player_2.score = p2_score
        game.remaining_moves = remining_moves
        if (noChars == "p1"):
            game.player_1.characters = []
        elif (noChars == "p2"):
            game.player_2.characters = []

        if game.get_current_player_name() == '':
            expected = {
                "player_2": game.player_2.user_name,
                "player_1": game.player_1.user_name,
                "score_1": game.player_1.score,
                "score_2": game.player_2.score,
                "arrows_1": game.player_1.arrows,
                "arrows_2": game.player_2.arrows,
                "board": game.board,
                "remaining_turns": game.remaining_moves,
                "game_id": game.game_id,
                "side": game.current_player.side,
                "result": "DRAW" if p1_score == p2_score else {
                    "WINNER": game.player_1.user_name if p2_score < p1_score else game.player_2.user_name,
                    "LOSER": game.player_2.user_name if p2_score < p1_score else game.player_1.user_name
                }
            }
        else:
            expected = {
                "player_2": game.player_2.user_name,
                "player_1": game.player_1.user_name,
                "score_1": game.player_1.score,
                "score_2": game.player_2.score,
                "arrows_1": game.player_1.arrows,
                "arrows_2": game.player_2.arrows,
                "board": game.board,
                "remaining_turns": game.remaining_moves,
                "game_id": game.game_id,
                "side": game.current_player.side,
            }
        self.assertEqual(game.generate_response(), expected)

    @parameterized.expand([
        ('shoot discovered opponent', 5, 1000, 8, 8, WEST, 8, 7, 17_000, 110_000, 4, "     "),
        ('shoot covered empty cell', 5, 1000, 8, 8, EAST, 8, 9, 1_100, 110_000, 4, "##F##"),
        ('shoot hole', 5, 1000, 8, 8, NORTH, 7, 8, 2000, 110_000, 4, "  O  "),
        ('shoot own char', 5, 1000, 8, 8, SOUTH, 9, 8, 0, 110_000, 4, "  L  "),
        ('shoot covered opponent', 4, 1000, 4, 4, WEST, 4, 3, 17_000, 110_000, 3, "     "),
        ('shoot discovered empty cell', 3, 1000, 4, 4, EAST, 4, 5, 1100, 110_000, 2, "  F  "),
        ('shoot covered opponent with treasures', 2, 1000, 4, 4, NORTH, 3, 4, 17_000, 30_000, 1, " 2 D "),
        ('shoot covered cell with treasures', 1, 1000, 4, 4, SOUTH, 5, 4, 1_100, 110_000, 0, "##F##"),
        ('shoot discovered opponent with treasures', 5, 1000, 0, 0, EAST, 0, 1, 17_000, 80_000, 4, " 3   "),
        ('shoot discovered cell with treasures', 5, 1000, 0, 0, SOUTH, 1, 0, 1_100, 110_000, 4, " 1F  ")
    ])
    def test_execute_action_shoot(self, name,
                                  initial_arrows, initial_score,
                                  from_row, from_col, direction,
                                  destination_row, destination_col,
                                  expected_own_score, expected_opponent_score,
                                  expected_arrows, expected_destination_cell):
        game = patched_game()

        board, shooter_player, shotted_player = generate_board_for_shoot_action_test()
        game.player_1 = shooter_player
        game.player_2 = shotted_player

        game._board._board = board
        game.current_player = game.player_1
        game.current_player.score = initial_score
        game.current_player.arrows = initial_arrows

        game.execute_action(SHOOT, from_row, from_col, direction)

        current_own_score = game.current_player.score
        current_opponent_score = game.player_2.score
        current_arrows = game.current_player.arrows
        destination_cell = game._board._board[destination_row][destination_col]

        self.assertEqual(current_own_score, expected_own_score)
        self.assertEqual(current_opponent_score, expected_opponent_score)
        self.assertEqual(current_arrows, expected_arrows)
        self.assertEqual(destination_cell.to_str(PLAYER_1), expected_destination_cell)

    @parameterized.expand([
        ('cell with hole',
         4, 4, WEST, 1000, 4, 3, 12_000, 3, EMPTY_CELL, '  O  ', 5),
        ('cell empty',
         4, 4, EAST, 1000, 4, 5, 12_000, 4, EMPTY_CELL, '  L  ', 5),
        ('cell with opponent char',
         4, 4, NORTH, 1000, 3, 4, 12_000, 3, EMPTY_CELL, '  R  ', 5),
        ('cell with own char',
         4, 4, SOUTH, 1000, 5, 4, 10_000, 4, '  L  ', '  L  ', 5),

        ('discovered cell with hole carrying treasure',
         8, 8, WEST, 1000, 8, 7, 2_000, 3, ' 1   ', '  O  ', 5),
        ('covered cell with treasures carrying treasure',
         8, 8, EAST, 1000, 8, 9, 92_000, 4, '     ', ' 3LD ', 5),
        ('covered cell with arrow',
         8, 8, NORTH, 1000, 7, 8, 12_000, 4, '     ', ' 1L  ', 6),
        ('covered cell with opponent charatcer carrying treasures',
         8, 8, SOUTH, 1000, 9, 8, 2000, 3, ' 1   ', '  R  ', 5),

    ])
    def test_execute_action_move(self, name,
                                 from_row, from_col, direction, initial_socre,
                                 destination_row, destination_col,
                                 expected_score, expected_remaining_characters,
                                 expected_initial_cell, expected_destination_cell,
                                 expected_arrows):
        game = patched_game()
        board, player_1, player_2 = generate_board_for_move_action_test()
        game.player_1 = player_1
        game.player_2 = player_2
        game.current_player = game.player_1
        game._board._board = board
        game.current_player.score = initial_socre

        game.execute_action(MOVE, from_row, from_col, direction)

        current_score = game.current_player.score
        current_remaining_characters = len(game.current_player.characters)
        current_arrows = game.current_player.arrows
        current_origin_cell = game._board._board[from_row][from_col].to_str(PLAYER_1)
        destination_cell = game._board._board[destination_row][destination_col].to_str(PLAYER_1)

        self.assertEqual(current_score, expected_score)
        self.assertEqual(current_origin_cell, expected_initial_cell)
        self.assertEqual(destination_cell, expected_destination_cell)
        self.assertEqual(current_remaining_characters, expected_remaining_characters)
        self.assertTrue(current_arrows, expected_arrows)

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

        self.assertEqual(actual_player.side, expected_player)
        self.assertEqual(actual_remaining_moves, expected_remainig_moves)

    def test_when_a_penalize_is_called_invalid_moves_count_increase(self):
        game = patched_game()
        player = game.player_1
        player.invalid_moves_count = 0
        game.penalize_player()

        self.assertEqual(player.invalid_moves_count, 1)

    def test_when_a_penalize_is_called_score_decreases(self):
        game = patched_game()
        player = game.player_1
        player._score = INITIAL_SCORE
        game.penalize_player()

        self.assertEqual(player._score, INITIAL_SCORE + SCORES[TIMEOUT_SC])

    def test_when_a_penalize_is_called_and_player_reaches_limit_invalids_games_end(self):
        game = patched_game()
        player = game.player_1
        player.invalid_moves_count = MAXIMUM_INVALID_MOVES - 1
        game.penalize_player()
        self.assertTrue(player.penalizated_for_invalid_moves)

    @parameterized.expand([
        (5, 3, 38, None, (True, GAME_OVER_MESSAGE_1)),
        (0, 5, 38, None, (True, GAME_OVER_MESSAGE_2)),
        (0, 0, 0, None, (True, GAME_OVER_MESSAGE_3)),
        (0, 0, 24, "p1", (True, GAME_OVER_MESSAGE_4)),
        (0, 0, 85, "p2", (True, GAME_OVER_MESSAGE_5)),
        (0, 0, 85, None, (False, GAME_OVER_NOT_MET)),  # Here, no game-over condition is met.
    ])
    def test_is_game_over(self, p1_invalids, p2_invalids, moves, noChars, message):
        users_names = [NAME_USER_1, NAME_USER_2]
        game = WumpusGame(users_names)
        game.player_1.invalid_moves_count = p1_invalids
        game.player_2.invalid_moves_count = p2_invalids
        game.remaining_moves = moves
        if (noChars == "p1"):
            game.player_1.characters = []
        elif (noChars == "p2"):
            game.player_2.characters = []
        self.assertEqual(game.is_game_over(), message)

    @parameterized.expand([
        ('try to move outside the board to west', 1, MOVE, WEST, 1, -1000),
        ('try to move outside the board north', 1, MOVE, NORTH, 1, -1000),
        ('try to shoot outside the board west', 1, SHOOT, WEST, 1, -1000),
        ('try to shoot outside the board north', 1, SHOOT, NORTH, 1, -1000),
        ('try to shoot without arrows', 0, SHOOT, EAST, 1, -1000),
    ])
    def test_execute_action_invalid(self, name,
                                    initial_arrows, action, direction,
                                    expected_invalid_moves, expected_score):
        board, player_1, player_2 = generate_board_for_shoot_action_test()

        game = patched_game()
        game.player_1 = player_1
        game.player_2 = player_2

        game._board._board = board
        game.current_player = game.player_1
        game.current_player.arrows = initial_arrows

        game.execute_action(action, 0, 0, direction)
        current_invalid_moves = game.current_player.invalid_moves_count
        current_score = game.current_player.score

        self.assertEqual(current_invalid_moves, expected_invalid_moves)
        self.assertEqual(current_score, expected_score)

    def test_get_current_player_name_else_remaining_moves(self):
        game = WumpusGame([NAME_USER_1, NAME_USER_2])
        game.remaining_moves = 0
        self.assertEqual(game.get_current_player_name(), '')

    def test_get_current_player_name_game_is_active(self):
        game = WumpusGame([NAME_USER_1, NAME_USER_2])
        game.game_is_active = False
        self.assertEqual(game.get_current_player_name(), '')


if __name__ == '__main__':
    unittest.main()
