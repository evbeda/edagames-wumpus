import unittest
from game.treasure import Treasure
from parameterized import parameterized


class TestTreasure(unittest.TestCase):

    @parameterized.expand([
        (50000,),
        (10000,)
    ])
    def test_treasure(self, value):
        treasure = Treasure()
        treasure.value = value
        self.assertEqual(treasure.value, value)
