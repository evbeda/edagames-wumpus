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

    @parameterized.expand([
        ((0, 1), 1, 0, PLAYER_1, False, False, 2),
        ((15, 8), 0, 0, PLAYER_2, True, False, 0),
    ])
    def test_cell_attributes(
        self,
        position,
        gold,
        diamond,
        player_name,
        has_hole,
        is_discover,
        arrow,
    ):
        cell = Cell()
        character = Character(Player(player_name))
        cell.position = position
        cell.gold = gold
        cell.diamond = diamond
        cell.character = character
        cell.has_hole = has_hole
        cell.is_discover = is_discover
        cell.arrow = arrow
        self.assertEqual(cell.position, position)
        self.assertEqual(cell.gold, gold)
        self.assertEqual(cell.diamond, diamond)
        self.assertEqual(cell.character, character)
        self.assertEqual(cell.has_hole, has_hole)
        self.assertEqual(cell.is_discover, is_discover)
        self.assertEqual(cell.arrow, arrow)
