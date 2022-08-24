import unittest
from game.game import WumpusGame
from parameterized import parameterized
from game.cell import Cell
from game.character import Character
from game.player import Player
from constans.constans import PLAYER_1, PLAYER_2


class TestCell(unittest.TestCase):
    def setUp(self):
        self.game = WumpusGame()

    @parameterized.expand([  # cell_attributes
        (0, 1, 1, 0, PLAYER_1, False, False, 2),
        (15, 8, 0, 0, PLAYER_2, True, False, 0),
    ])
    def test_cell_attributes(
        self,
        row,
        col,
        gold,
        diamond,
        player_name,
        has_hole,
        is_discover,
        arrow,
    ):
        cell = Cell(row, col)
        character = Character(Player(player_name))
        cell.gold = gold
        cell.diamond = diamond
        cell.character = character
        cell.has_hole = has_hole
        cell.is_discover = is_discover
        cell.arrow = arrow
        self.assertEqual(cell.gold, gold)
        self.assertEqual(cell.diamond, diamond)
        self.assertEqual(cell.character, character)
        self.assertEqual(cell.has_hole, has_hole)
        self.assertEqual(cell.is_discover, is_discover)
        self.assertEqual(cell.arrow, arrow)

    @parameterized.expand([
        (0, 0, None, False, 0, True),
        (1, 0, None, False, 0, False),
        (4, 0, None, False, 0, False),
        (0, 1, None, False, 0, False),
        (0, 0, Player(PLAYER_1), False, 0, False),
        (0, 1, None, True, 0, False),
        (0, 1, None, False, 1, False),
    ])
    def test_cell_is_empty(self, gold, diamond,
                           character, has_hole, arrow,
                           expected):

        cell = Cell(0, 0)
        cell.gold = gold
        cell.diamond = diamond
        cell.character = character
        cell.has_hole = has_hole
        cell.arrow = arrow

        self.assertEqual(cell.empty, expected)
<<<<<<< HEAD

    @parameterized.expand([  # cell set_character_when_move
        (PLAYER_1, 1, 3),
        (PLAYER_2, 0, 4)
    ])
    def test_cell_set_character_when_move(self, player_name, diamond, gold):
        cell = Cell(0, 0)
        character = Character(Player(player_name))
        character.diamonds = diamond
        character.golds = gold
        cell.set_character_when_move(character)
        self.assertEqual(cell.diamond, character.diamonds)
        self.assertEqual(cell.gold, character.golds)
=======
>>>>>>> place golds method
