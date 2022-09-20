import unittest
from game.manager import Manager


class TestManager(unittest.TestCase):

    def test_manager_init(self):
        # useless test, only instanciates manager
        manager = Manager()
        self.assertDictEqual(manager.games, {})
        self.assertDictEqual(manager.action_data, {})
