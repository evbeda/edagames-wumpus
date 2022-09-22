import unittest
from constans.scenarios import (
    TESTED_CELL_1, TESTED_CELL_10, TESTED_CELL_2,
    TESTED_CELL_3, TESTED_CELL_4, TESTED_CELL_5,
    TESTED_CELL_6, TESTED_CELL_7, TESTED_CELL_8, TESTED_CELL_9
)
from game.diamond import Diamond
from game.gold import Gold
from game.game import WumpusGame
from parameterized import parameterized
from game.cell import Cell
from game.character import Character
from game.player import Player
from constans.constans import EMPTY_CELL, HIDDEN_CELL, PLAYER_1, PLAYER_2, NAME_USER_1, NAME_USER_2


class TestCell(unittest.TestCase):

    @parameterized.expand([  # cell_attributes
        (0, 1, PLAYER_1, False, [False, False], 2, Gold(), Diamond()),
        (15, 8, PLAYER_2, True, [False, False], 0, "", "",),
    ])
    def test_cell_attributes(
        self,
        row,
        col,
        player_name,
        has_hole,
        is_discover,
        arrow,
        treasure1,
        treasure2,
    ):
        cell = Cell(row, col)
        character = Character(Player(player_name, NAME_USER_1))
        cell.treasures.append(treasure1)
        cell.treasures.append(treasure2)
        cell.character = character
        cell.has_hole = has_hole
        cell.is_discover = is_discover
        cell.arrow = arrow
        self.assertEqual(cell.treasures[0], treasure1)
        self.assertEqual(cell.treasures[1], treasure2)
        self.assertEqual(cell.character, character)
        self.assertEqual(cell.has_hole, has_hole)
        self.assertEqual(cell.is_discover[0], is_discover[0])
        self.assertEqual(cell.is_discover[1], is_discover[1])
        self.assertEqual(cell.arrow, arrow)

    @parameterized.expand([
        ([], None, False, 0, True),
        ([Gold()], None, False, 0, False),
        ([Gold(), Gold(), Gold(), Gold(), Gold()], None, False, 0, False),
        ([Diamond()], None, False, 0, False),
        ([], Player(PLAYER_1, NAME_USER_1), False, 0, False),
        ([Diamond()], None, True, 0, False),
        ([Diamond()], None, False, 1, False),
    ])
    def test_cell_is_empty(self, treasure,
                           character, has_hole, arrow,
                           expected):

        cell = Cell(0, 0)
        cell.treasures = treasure
        cell.character = character
        cell.has_hole = has_hole
        cell.arrow = arrow

        self.assertEqual(cell.empty, expected)

    @parameterized.expand([
        (0, 0, Player(PLAYER_1, NAME_USER_1), True),
        (0, 0, None, False),
    ])
    def test_cell_there_arent_player(self, row, col,
                                     player,
                                     expected):
        cell = Cell(row, col)
        character_1 = player
        cell.character = character_1
        self.assertEqual(cell.are_there_player, expected)

    @parameterized.expand([
        (0, 0, PLAYER_1),
        (0, 1, None),
        (0, 16, PLAYER_2),
        (1, 15, None)
    ])
    def test_has_player_property(self, row, col, expected):
        users_names = [NAME_USER_1, NAME_USER_2]
        game = WumpusGame(users_names)
        cell = game._board._board[row][col]
        result = cell.has_player
        self.assertEqual(result, expected)

    @parameterized.expand([
        (PLAYER_1, TESTED_CELL_1, HIDDEN_CELL),
        (PLAYER_1, TESTED_CELL_2, EMPTY_CELL),
        (PLAYER_2, TESTED_CELL_2, HIDDEN_CELL),
        (PLAYER_1, TESTED_CELL_3, '  P  ',),
        (PLAYER_2, TESTED_CELL_4, '  P  ',),
        (PLAYER_2, TESTED_CELL_4, '  P  ',),
        (PLAYER_2, TESTED_CELL_5, '  O  ',),
        (PLAYER_2, TESTED_CELL_6, '  F  ',),
        (PLAYER_2, TESTED_CELL_7, ' 2   ',),
        (PLAYER_1, TESTED_CELL_8, '   D ',),
        (PLAYER_1, TESTED_CELL_9, ' 1 D ',),
        (PLAYER_1, TESTED_CELL_10, '##F##',),
        (PLAYER_2, TESTED_CELL_10, '##F##',),
    ])
    def test_cell_representation(self, player, cell: Cell, expected):
        self.assertEqual(cell.to_str(player), expected)

    def test_remove_character(self):
        users_names = [NAME_USER_1, NAME_USER_2]
        game = WumpusGame(users_names)
        cell_player = game._board._board[0][0]
        cell_player.remove_character()
        self.assertIsNone(cell_player.character)
        self.assertEqual(len(game.current_player.characters), 2)


if __name__ == "__main__":
    unittest.main()
