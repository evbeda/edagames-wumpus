import unittest
from parameterized import parameterized
from constans.constans import PLAYER_1, PLAYER_2, NAME_USER_1, NAME_USER_2
from game.character import Character
from game.player import Player


class TestCharacter(unittest.TestCase):
    def setUp(self):
        pass

    @parameterized.expand([
        (PLAYER_1, NAME_USER_1),
        (PLAYER_2, NAME_USER_2),
    ])
    def test_initial_character(self, player_name, name_user):
        char = Character(Player(player_name, name_user))
        self.assertEqual(char.gold, 0)
        self.assertEqual(char.gold, 0)
        self.assertEqual(char.player.name, player_name)


if __name__ == "__main__":
    unittest.main()
