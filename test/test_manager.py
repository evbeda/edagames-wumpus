import unittest
from unittest.mock import patch
from test.test_game import patched_game
from game.manager import Manager
from parameterized import parameterized
from constans.constans import (
    ACTION,
    COL,
    DATA,
    DIRECTION_MESSAGE,
    EAST,
    NORTH,
    MESSAGE_DATA_KEYS,
    MOVE,
    SOUTH,
    ROW,
    WEST
)
from exceptions.personal_exceptions import (
    InvalidData,
    InvalidKey
)


class TestManager(unittest.TestCase):

    def test_manager_init(self):
        # useless test, only instanciates manager
        manager = Manager()
        self.assertDictEqual(manager.games, {})
        self.assertDictEqual(manager.action_data, {})

    @parameterized.expand([
        ('NORTH position', NORTH),
        ('EAST position', EAST),
        ('SOUTH position', SOUTH),
        ('WEST position', WEST),
    ])
    def test_get_correct_data_correct(self, name, position):
        manager = Manager()
        data_message = {
            'from_row': 0,
            'from_col': 4,
            'direction': position
        }
        expected_result = {
            'from_row': 0,
            'from_col': 4,
            'direction': position
        }
        result = manager.get_correct_data(data_message, MESSAGE_DATA_KEYS)
        self.assertEqual(result, expected_result)

    @parameterized.expand(
        [
            (
                'InvalidData exception number',
                {'from_row': 0,
                 'from_col': 'a',
                 'direction': NORTH},
                InvalidData,
            ),
            (
                'InvalidData exception direction',
                {'from_row': 0,
                 'from_col': 4,
                 'direction': "WUMPUS"},
                InvalidData
            ),
            (
                'InvalidData exception direction int',
                {'from_row': 0,
                 'from_col': 4,
                 'direction': 1},
                InvalidData
            ),
            (
                'InvalidData exception direction boolean',
                {'from_row': 0,
                 'from_col': 4,
                 'direction': True},
                InvalidData
            ),
            (
                'InvalidData exception direction boolean',
                {'from_row': 0,
                 'from_col': True,
                 'direction': NORTH},
                InvalidData
            ),
            (
                'InvalidKey exception from_col',
                {'from_row': 0,
                 'from_cols': 4,
                 'direction': NORTH},
                InvalidKey
            ),
            (
                'InvalidKey exception from_row',
                {'from_rasdasdows': 0,
                 'from_col': 4,
                 'direction': NORTH},
                InvalidKey
            ),
            (
                'InvalidKey exception direction',
                {'from_row': 0,
                 'from_cols': 4,
                 'Directuiasd': NORTH},
                InvalidKey
            ),
        ]
    )
    def test_get_correct_data_exception(self, name, data_message, expection):
        manager = Manager()
        with self.assertRaises(expection):
            manager.get_correct_data(data_message, MESSAGE_DATA_KEYS)

    @patch('game.game.WumpusGame.execute_action')
    def test_execute_action_manager(self, mock_execute_action):
        manager = Manager()
        game = patched_game()
        api_data = dict(
            {
                ACTION: MOVE,
                DATA: {
                    ROW: 0,
                    COL: 4,
                    DIRECTION_MESSAGE: NORTH
                }
            }
        )
        manager.execute_action_manager(game, api_data)
        mock_execute_action.assert_called_once_with(
            MOVE,
            0,
            4,
            NORTH
        )

    def test_execute_action_manager_raise(self):
        manager = Manager()
        game = patched_game()
        api_data = dict(
            {
                ACTION: "WUMPUS",
                DATA: {
                    ROW: 0,
                    COL: 4,
                    DIRECTION_MESSAGE: NORTH
                }
            }
        )
        with self.assertRaises(InvalidData):
            manager.execute_action_manager(game, api_data)

    def test_execute_action_manager_raise_key(self):
        manager = Manager()
        game = patched_game()
        api_data = dict(
            {
                "Wumpus": MOVE,
                DATA: {
                    ROW: 0,
                    COL: 4,
                    DIRECTION_MESSAGE: NORTH
                }
            }
        )
        with self.assertRaises(InvalidData):
            manager.execute_action_manager(game, api_data)
