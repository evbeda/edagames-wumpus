import unittest
from game.treasure import Treasure
from parameterized import parameterized
from constans.constans import SCORES
from game.gold import Gold
from game.diamond import Diamond


class TestTreasure(unittest.TestCase):

    @parameterized.expand([
        (50000,),
        (10000,)
    ])
    def test_treasure(self, value):
        treasure = Treasure()
        treasure.value = value
        self.assertEqual(treasure.value, value)

    def test_gold(self):
        gold = Gold()
        self.assertEqual(gold.value, SCORES["GOLD"])

    def test_diamond(self):
        gold = Diamond()
        self.assertEqual(gold.value, SCORES["DIAMOND"])


if __name__ == "__main__":
    unittest.main()
