from copy import deepcopy
import unittest
from unittest.mock import MagicMock, patch
from parameterized import parameterized
from game.diamond import Diamond

from game.game import WumpusGame
from constans.constans import EMPTY_CELL, PLAYER_1, PLAYER_2
from constans.constants_utils import MOVE, SHOOT, WEST, EAST, SOUTH, NORTH
from constans.constants_game import (
    DIAMOND,
    GOLD_QUANTITY,
    HOLE,
    HOLE_QUANTITY,
    LARGE,
    MIDDLE,
    GOLD,
)
from game.cell import Cell
from game.character import Character
from game.gold import Gold
from game.player import Player

from constans.constants_scores import (
    CORRECT_MOVE,
    DEATH,
    INVALID_MOVE,
    ARROW_MISS,
    GET_ITEMS,
    KILL,
    TIMEOUT,
    SCORES,
)
from constans.scenarios import (
    BOARD_FOR_MOVE_AND_MODIFY_SCORE,
    CLOSED_GOLD_BOARD,
    DANGER_SIGNAL_SCENARIO,
    DICT_FILTER_MOVE_MK,
    DICTIONARY_ENE,
    DICTIONARY_H,
    DICTIONARY_MAK_MOV,
    DICTIONARY_MAK_MOV_P2,
    FILTER_MOVE_BOARD_ENE,
    FILTER_MOVE_BOARD_H,
    FILTER_MOVE_MAKE_MOVE,
    FIN_FILTER_MOVE_BOARD_ENE,
    FIN_FILTER_MOVE_BOARD_H,
    FIN_FILTER_MOVE_MAKE_MOVE,
    FIND_GOLD_POS_1,
    FIND_GOLD_POS_2,
    FIND_GOLD_POS_3,
    FIND_GOLD_POS_4,
    INITIAL_BIG_FAIL_BOARD,

    MAKE_MOVE_BOARD,
    MAKE_MOVE_BOARD_P2,

    PARSE_CELL_SCENARIO,
    PARSE_CELL_SCENARIO_STR_PLAYER_1,
    PARSE_CELL_SCENARIO_STR_PLAYER_2,

    RECURSIVE,
    RECURSIVE_SIDE,
    RECURSIVE_SIDE_CORNER,
    TEST_BOARD_INIT_PLAYER_1,
    TEST_BOARD_INIT_PLAYER_2,
    WAY_GOLD_TWO_PLAYERS,
    VALID_HOLE_SCENARIO,
)
from game.utils import posibles_positions
from exceptions.personal_exceptios import (moveToYourOwnCharPositionException,
                                           notYourCharacterException,
                                           noPossibleMoveException,)


def patched_game() -> WumpusGame:
    with patch.object(WumpusGame, '_valid_hole', return_value=True):
        game = WumpusGame()
    return game


class TestGame(unittest.TestCase):

    def test_create_game(self):
        # check game attributes creation
        game = patched_game()
        self.assertIsNotNone(game._board)
        self.assertIsNotNone(game._board[0][0])
        self.assertIsInstance(game._board[0][0], Cell)
        self.assertEqual(game.player_1.name, PLAYER_1)
        self.assertEqual(game.player_2.name, PLAYER_2)
        self.assertTrue(game)

    def test_board_size(self):
        game = patched_game()
        self.assertEqual(len(game._board), LARGE)
        self.assertEqual(len(game._board[0]), LARGE)

    def test_move_player_to_other_player_position(self):
        game = patched_game()
        cel_player = Cell(5, 5)
        cel_character = Character(PLAYER_1)
        cel_player.character = cel_character
        game._board[5][5] = cel_player
        with self.assertRaises(moveToYourOwnCharPositionException):
            game.move_to_own_character_position(PLAYER_1, 5, 5)

    def test_place_character_initial_pos_player_1(self):
        game = patched_game()
        game._board = [
            [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)
        ]
        player = Player(PLAYER_1)
        character1 = Character(player)
        character2 = Character(player)
        character3 = Character(player)
        game.place_character_initial_pos(
            player,
            character1,
            character2,
            character3
        )
        self.assertEqual(game._board[0][0].character, character1)
        self.assertEqual(game._board[8][0].character, character2)
        self.assertEqual(game._board[16][0].character, character3)

    def test_place_character_initial_pos_player_2(self):
        game = patched_game()
        game._board = [
            [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)
        ]
        player = Player(PLAYER_2)
        character1 = Character(player)
        character2 = Character(player)
        character3 = Character(player)
        game.place_character_initial_pos(
            player,
            character1,
            character2,
            character3
        )
        self.assertEqual(game._board[0][16].character, character1)
        self.assertEqual(game._board[8][16].character, character2)
        self.assertEqual(game._board[16][16].character, character3)

    def test_place_gold(self):
        game = patched_game()
        game._board = [
                [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)
            ]
        game.place_items(GOLD, GOLD_QUANTITY)

        gold_quantity = sum([cell.gold
                            for row_cell in game._board
                            for cell in row_cell])

        golds_first_half = sum([game._board[row][col].gold
                                for col in range(MIDDLE)
                                for row in range(LARGE)])
        golds_second_half = sum([game._board[row][col].gold
                                for col in range(MIDDLE + 1, LARGE)
                                for row in range(LARGE)])

        self.assertEqual(gold_quantity, 16)
        self.assertEqual(golds_first_half, 8)
        self.assertEqual(golds_second_half, 8)

    def test_place_gold_position(self):

        gold_places = [(1, 1), (5, 0), (11, 0), (14, 4), (11, 5),
                       (10, 7), (5, 5), (1, 3), (15, 15), (15, 12),
                       (10, 12), (7, 11), (4, 9), (0, 15), (1, 12),
                       (6, 9)]
        gold_places_patch = sum(gold_places, ())
        game = patched_game()
        with patch('random.randint', side_effect=list(gold_places_patch)):
            game._board = [
                [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)
            ]
            game.place_items(GOLD, GOLD_QUANTITY)
            golds = [
                (row, col)
                for row, row_cell in enumerate(game._board)
                for col, cell in enumerate(row_cell)
                if cell.gold > 0]
            self.assertEqual(sorted(gold_places), sorted(golds))

    @parameterized.expand([
        (4, 1)
    ])
    def test_initial_diamond_position(self, row_random, expected_result):
        game = patched_game()
        mid_col = LARGE//2
        with patch('random.randint', return_value=row_random):
            game.initial_diamond_position()
        self.assertEqual(game._board[row_random][mid_col].diamond,
                         expected_result)

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

    def test_place_holes(self):
        holes_positions = [
            (0, 3), (1, 2), (3, 4),
            (7, 6), (10, 3), (12, 1),
            (14, 1), (15, 11), (1, 13),
            (4, 13), (7, 15), (9, 12),
            (13, 15), (14, 9), (15, 15),
            (3, 14)]

        hole_places_patch = sum(holes_positions, ())
        game = patched_game()
        with patch('random.randint', side_effect=list(hole_places_patch)):
            game._board = [
                [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)
            ]
            game.place_items(HOLE, HOLE_QUANTITY)
            holes = [
                position for position in holes_positions if (
                    game._board[position[0]][position[1]].has_hole is True
                    )
            ]
            self.assertEqual(sorted(holes_positions), sorted(holes))

    def test_holes_quantity(self):
        game = patched_game()
        game._board = [
                [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)
            ]
        game.place_items(HOLE, HOLE_QUANTITY)

        hole_quantity = sum([cell.has_hole
                            for row_cell in game._board
                            for cell in row_cell])

        holes_first_half = sum([game._board[row][col].has_hole
                                for col in range(MIDDLE)
                                for row in range(LARGE)])
        holes_second_half = sum([game._board[row][col].has_hole
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
    def test_can_find_gold(self, char_position, gold_position,
                           board, expected):
        game = patched_game()
        game._board = deepcopy(board)
        row, col = char_position
        result = game._can_find_gold(row, col, gold_position, [])
        self.assertEqual(result, expected)

    @parameterized.expand([
        (PLAYER_1, 0, 1),
    ])
    def test_discover_cell_player_1(self, player, row, col):
        game = patched_game()
        character = Character(Player(player))
        cell = game._board[row][col]
        cell.character = character
        game.discover_cell(row, col)
        result = cell.is_discover[0]
        self.assertEqual(result, True)

    @parameterized.expand([
        (PLAYER_2, 0, 15)
    ])
    def test_discover_cell_player_2(self, player, row, col):
        game = patched_game()
        game.change_current_player()
        character = Character(Player(player))
        cell = game._board[row][col]
        cell.character = character
        game.discover_cell(row, col)
        result = cell.is_discover[1]
        self.assertEqual(result, True)

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
        game = patched_game()
        game._board = deepcopy(VALID_HOLE_SCENARIO)
        self.assertEqual(game._valid_hole(row, col), expected)

    @parameterized.expand([
        (PLAYER_1, PLAYER_2, 0, 0, 0, 1)
    ])
    def test_is_valid_move_not_your_character(self, p1, p2,
                                              from_row, from_col,
                                              to_row, to_col):
        game = WumpusGame()
        player_1 = Player(p1)
        player_2 = Player(p2)
        character_1_of_player_1 = player_1.characters[0]
        game._board[from_row][from_col].character = character_1_of_player_1
        game.current_player = player_1
        with self.assertRaises(notYourCharacterException):
            game.is_valid_move(from_row, from_col,
                               to_row, to_col, player_2)

    @parameterized.expand([
        (PLAYER_1, 0, 0, -1, 0),
        (PLAYER_1, 0, 0, 3, 0),
        (PLAYER_1, 0, 0, 0, 0),
    ])
    def test_is_valid_move_not_possible_move(self, p1,
                                             from_row, from_col,
                                             to_row, to_col):
        game = WumpusGame()
        player_1 = Player(p1)
        character_1_of_player_1 = player_1.characters[0]
        game._board[from_row][from_col].character = character_1_of_player_1
        game.current_player = player_1
        with self.assertRaises(noPossibleMoveException):
            game.is_valid_move(from_row, from_col,
                               to_row, to_col, player_1)

    @parameterized.expand([
        (PLAYER_1, 0, 0, 0, 1),
    ])
    def test_is_valid_move_to_a_same_character(self, P1, from_row, from_col,
                                               to_row, to_col):
        game = WumpusGame()
        player_1 = Player(P1)
        character_1_of_player_1 = player_1.characters[0]
        character_2_of_player_1 = player_1.characters[1]
        game._board[from_row][from_col].character = character_1_of_player_1
        game._board[to_row][to_col].character = character_2_of_player_1
        game.current_player = player_1
        with self.assertRaises(moveToYourOwnCharPositionException):
            game.is_valid_move(from_row, from_col,
                               to_row, to_col, player_1)

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
        game = WumpusGame()
        player_1 = Player(P1)
        player_2 = Player(P2)
        character_1_of_player_1 = player_1.characters[0]
        character_1_of_player_2 = player_2.characters[0]
        game._board[c1_row][c1_col].character = character_1_of_player_1
        game._board[c2_row][c2_col].character = character_1_of_player_2
        expected_result['player'] = player_1
        game.current_player = player_1
        game.filter_move = MagicMock()
        game.is_valid_move(c1_row, c1_col,
                           to_row, to_col, player_1)
        game.filter_move.assert_called_once()
        game.filter_move.assert_called_once_with(expected_result)

    @parameterized.expand([
        (PLAYER_1, 4, 3, EMPTY_CELL, '~    ', ),
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
        game._board = deepcopy(DANGER_SIGNAL_SCENARIO)

        game._board[2][2].character = Character(game.player_1)
        game._board[2][3].character = Character(game.player_1)
        game._board[2][4].character = Character(game.player_2)

        game._board[7][0].character = Character(game.player_2)
        game._board[7][1].character = Character(game.player_2)
        game._board[7][2].character = Character(game.player_1)

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

    @parameterized.expand([  # case for filter event
        (DICTIONARY_H, FILTER_MOVE_BOARD_H,
         FIN_FILTER_MOVE_BOARD_H, [
            Gold(), Gold(), Gold(), Gold(), Gold(), Diamond()
            ], 5, 1),
        (DICTIONARY_ENE, FILTER_MOVE_BOARD_ENE,
         FIN_FILTER_MOVE_BOARD_ENE, [
            Gold(), Gold(), Gold(), Gold(), Gold(), Diamond()
            ], 5, 1),
        (DICT_FILTER_MOVE_MK, FILTER_MOVE_MAKE_MOVE,
         FIN_FILTER_MOVE_MAKE_MOVE, [], 0, 0)
    ])
    def test_filter_move(self, dictionary, initial_board,
                         finalboard, treasure, count_gold, count_diam):
        game = WumpusGame()
        game._board = initial_board
        game.filter_move(dictionary)
        cell = finalboard[dictionary["from_row"]][dictionary["from_col"]]
        cell.treasures = treasure
        gold_cel = cell.gold
        diam_cel = cell.diamond
        diam_char = cell.character
        self.assertEqual(gold_cel, count_gold)
        self.assertEqual(diam_cel, count_diam)
        self.assertIsNone(diam_char)

    @parameterized.expand([  # after verify all posibilities make move
         (DICTIONARY_MAK_MOV, MAKE_MOVE_BOARD,
          3, 0, 0, 0, True, False, 2, 0),
    ])
    def test_make_move_P1(self, dictionary, initial_board,
                          gold_new, gold_old, diamond_new,
                          diamond_old, is_visited_p1,
                          is_visited_p2, new_arrows, old_arrow):
        game = WumpusGame()
        game._board = initial_board
        game.make_move(dictionary)

        new_cell: Cell = game._board[
            dictionary["to_row"]][dictionary["to_col"]]
        player_character: Character = game.\
            _board[dictionary["to_row"]][dictionary["to_col"]].character
        old_cell: Cell = game._board[
            dictionary["from_row"]][dictionary["from_col"]]

        self.assertEqual(new_cell.is_discover[0], is_visited_p1)
        self.assertEqual(new_cell.is_discover[1], is_visited_p2)
        self.assertEqual(new_cell.arrow, old_arrow)
        self.assertEqual(new_cell.gold, gold_old)
        self.assertEqual(new_cell.diamond, diamond_old)
        self.assertEqual(old_cell.arrow, old_arrow)
        self.assertEqual(old_cell.gold, gold_old)
        self.assertEqual(old_cell.diamond, diamond_old)
        self.assertIsNotNone(player_character)
        self.assertEqual(player_character.gold, gold_new)
        self.assertEqual(player_character.diamond, diamond_new)
        self.assertEqual(player_character.player.arrows, new_arrows)

    @parameterized.expand([  # after verify all posibilities make move
         (DICTIONARY_MAK_MOV_P2, MAKE_MOVE_BOARD_P2,
          5, 0, 1, 0, False, True, 3, 0)
    ])
    def test_make_move_P2(self, dictionary, initial_board,
                          gold_new, gold_old, diamond_new,
                          diamond_old, is_visited_p1,
                          is_visited_p2, new_arrows, old_arrow):
        game = WumpusGame()
        game._board = initial_board
        game.change_current_player()
        game.make_move(dictionary)

        new_cell: Cell = game._board[
            dictionary["to_row"]][dictionary["to_col"]]
        player_character: Character = game.\
            _board[dictionary["to_row"]][dictionary["to_col"]].character
        old_cell: Cell = game._board[
            dictionary["from_row"]][dictionary["from_col"]]

        self.assertEqual(new_cell.is_discover[0], is_visited_p1)
        self.assertEqual(new_cell.is_discover[1], is_visited_p2)
        self.assertEqual(new_cell.arrow, old_arrow)
        self.assertEqual(new_cell.gold, gold_old)
        self.assertEqual(new_cell.diamond, diamond_old)
        self.assertEqual(old_cell.arrow, old_arrow)
        self.assertEqual(old_cell.gold, gold_old)
        self.assertEqual(old_cell.diamond, diamond_old)
        self.assertIsNotNone(player_character)
        self.assertEqual(player_character.gold, gold_new)
        self.assertEqual(player_character.diamond, diamond_new)
        self.assertEqual(player_character.player.arrows, new_arrows)

    @parameterized.expand([
        (0, 0, PLAYER_2, '  P  '),
        (0, 16, PLAYER_1, '  B  '),
        (8, 0, PLAYER_2, '  P +'),
        (8, 1, PLAYER_1, '  B +'),
        (10, 11, PLAYER_1, '~ B +'),
        (10, 10, PLAYER_2, '~ P +'),
        (4, 8, PLAYER_2, '~   +'),
        (7, 2, PLAYER_1, '#####'),
        (7, 3, PLAYER_1, '#####'),
        (7, 3, PLAYER_1, '#####'),
        (4, 4, PLAYER_1, '##F##'),
        (4, 5, PLAYER_1, '##F##'),
        (4, 6, PLAYER_1, '##F##'),
        (4, 7, PLAYER_1, '  O  '),
        (4, 9, PLAYER_2, '  F  '),
        (14, 5, PLAYER_2, ' 3F  '),
        (14, 6, PLAYER_2, ' 3FD '),
    ])
    def test_parse_cell(self, row, col, player_name, expected):
        game: WumpusGame = patched_game()
        game._board = PARSE_CELL_SCENARIO
        if PLAYER_1 == player_name:
            game.current_player = game.player_1
        else:
            game.current_player = game.player_2
        self.assertEqual(game._parse_cell(row, col), expected)

    def test_make_move_and_modify_score(self):
        game = WumpusGame()
        game._board = BOARD_FOR_MOVE_AND_MODIFY_SCORE

        character = Character(game.player_1)
        game.player_1.characters.append(character)
        game._board[4][5].character = character
        dict_move = {
            "from_col": 5,
            "from_row": 4,
            "to_col": 5,
            "to_row": 5,
            "player": game.current_player
        }
        gold_before_move = character.gold
        diamonds_before_move = character.diamond

        game.make_move(dict_move)

        golds_after_move = character.gold
        diamonds_after_move = character.diamond

        expected_score = (SCORES[GOLD] * 2 + SCORES[DIAMOND] +
                          SCORES[CORRECT_MOVE])

        self.assertEqual(gold_before_move, 0)
        self.assertEqual(diamonds_before_move, 0)
        self.assertEqual(golds_after_move, 2)
        self.assertEqual(diamonds_after_move, 1)
        self.assertEqual(game.player_1.score, expected_score)

    @parameterized.expand([
        (PLAYER_2, TEST_BOARD_INIT_PLAYER_2),
        (PLAYER_1, TEST_BOARD_INIT_PLAYER_1)
    ])
    def test_init_board(self, current_player, expected_board):
        game = WumpusGame()

        if PLAYER_1 == current_player:
            game.current_player = game.player_1
        else:
            game.current_player = game.player_2
        self.assertEqual(game.board, expected_board)

    @parameterized.expand([
        (PLAYER_2, PARSE_CELL_SCENARIO_STR_PLAYER_2),
        (PLAYER_1, PARSE_CELL_SCENARIO_STR_PLAYER_1)
    ])
    def test_board(self, curent_player, expected_board):
        game = patched_game()
        if PLAYER_1 == curent_player:
            game.current_player = game.player_1
        else:
            game.current_player = game.player_2
        self.maxDiff = None
        game._board = deepcopy(PARSE_CELL_SCENARIO)
        self.assertEqual(game.board, expected_board)

    # @parameterized.expand([  # test raise exception
    #     (0, 0, MOVE, WEST),
    #     (0, 16, MOVE, EAST),
    #     (0, 0, MOVE, NORTH),
    #     (16, 0, MOVE, SOUTH),
    #     (0, 0, SHOOT, WEST),
    #     (0, 16, SHOOT, EAST),
    #     (0, 0, SHOOT, NORTH),
    #     (16, 0, SHOOT, SOUTH),
    # ])
    # def test_action_manager_raise_exception(
    #     self,
    #     initial_row,
    #     initial_col,
    #     action,
    #     direction
    # ):
    #     game = WumpusGame()
    #     with self.assertRaises(Exception):
    #         game.action_manager(action, initial_row, initial_col, direction)

    @parameterized.expand([  # test action manager
        (0, 0, MOVE, EAST),
        (8, 0, MOVE, EAST),
        (16, 0, MOVE, NORTH),
    ])
    def test_action_manager_move(
        self,
        initial_row,
        initial_col,
        action,
        direction
    ):
        game = WumpusGame()
        game.is_valid_move = MagicMock()
        game.action_manager(action, initial_row, initial_col, direction)
        game.is_valid_move.assert_called_once()

    @parameterized.expand([  # test action manager
        (0, 16, SHOOT, WEST),
        (8, 16, SHOOT, SOUTH),
        (16, 16, SHOOT, NORTH),
    ])
    def test_action_manager_shoot(
        self,
        initial_row,
        initial_col,
        action,
        direction
    ):
        game = WumpusGame()
        game.change_current_player()
        game.shoot_arrow = MagicMock()
        game.action_manager(action, initial_row, initial_col, direction)
        game.shoot_arrow.assert_called_once()
        game.shoot_arrow.assert_called_once_with(
            initial_row,
            initial_col,
            direction
        )


if __name__ == '__main__':
    unittest.main()
