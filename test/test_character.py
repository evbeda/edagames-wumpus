import unittest
from parameterized import parameterized
from constans.constans import PLAYER_1, PLAYER_2
from game.character import Character
from game.player import Player


class TestCharacter(unittest.TestCase):
    def setUp(self):
        pass

    @parameterized.expand([
        PLAYER_1,
        PLAYER_2
    ])
    def test_initial_character(self, player_name):
        char = Character(Player(player_name))
        self.assertEqual(char.golds, 0)
        self.assertEqual(char.golds, 0)
        self.assertEqual(char.player.name, player_name)


if __name__ == "__main__":
    unittest.main()
