import unittest
from unittest.mock import patch
from edagames_grpc.game_start import GameStart
from edagames_grpc.game_state import GameState
from game.game import WumpusGame
from test.test_game import patched_game
from game.manager import Manager
from parameterized import parameterized
from constans.constans import (
    ACTION,
    COL,
    DATA,
    DIRECTION_MESSAGE,
    EAST,
    GAMEOVER_STATE,
    INVALID_PENALIZE,
    NORTH,
    MESSAGE_DATA_KEYS,
    MOVE,
    ROW,
    SOUTH,
    STATE,
    TIMEOUT,
    WEST,
    NAME_USER_1,
    NAME_USER_2
)
from exceptions.personal_exceptions import (
    InvalidData,
    InvalidKey,
    InvalidQuantityPlayers,
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

    def test_delete_game_from_manager(self):
        manag = Manager()
        users_names = [NAME_USER_1, NAME_USER_2]
        game = WumpusGame(users_names)
        game_id = "123asd"
        manag.games[game_id] = game
        manag.delete_game_from_manager(game_id)
        self.assertEqual({}, manag.games)

    def test_check_game_over_false(self):
        manag = Manager()
        users_names = [NAME_USER_1, NAME_USER_2]
        game = WumpusGame(users_names)
        game_id = "123asd"
        game.game_id = game_id
        manag.games[game_id] = game
        self.assertFalse(manag.check_game_over(game))

    @patch('game.manager.Manager.delete_game_from_manager')
    def test_check_game_over_without_moves(self, moke_delete_game):
        manag = Manager()
        users_names = [NAME_USER_1, NAME_USER_2]
        game = WumpusGame(users_names)
        game_id = "123asd"
        game.game_id = game_id
        game.remaining_moves = 0
        manag.games[game_id] = game
        manag.check_game_over(game)
        moke_delete_game.assert_called_once_with(game_id)
        self.assertTrue(manag.check_game_over(game))

    @patch('game.manager.Manager.delete_game_from_manager')
    def test_check_game_over_game_over(self, moke_delete_game):
        manag = Manager()
        users_names = [NAME_USER_1, NAME_USER_2]
        game = WumpusGame(users_names)
        game_id = "123asd"
        game.game_id = game_id
        game.game_is_active = False
        manag.games[game_id] = game
        manag.check_game_over(game)
        moke_delete_game.assert_called_once_with(game_id)
        self.assertTrue(manag.check_game_over(game))

    def test_create_game(self):
        with patch('game.manager.Manager.get_game_start', return_value=True):
            manager = Manager()
            players_names = ['bot1', 'bot2']
            self.assertTrue(manager.create_game(players_names))

    def test_create_game_error(
        self,
    ):
        manager = Manager()
        players_names = ['bot1']
        with self.assertRaises(InvalidQuantityPlayers):
            manager.create_game(players_names)

    def test_get_game_start(self):
        manager = Manager()
        game_start = manager.get_game_start(
            WumpusGame([NAME_USER_1, NAME_USER_2]),
        )
        self.assertIsInstance(
            game_start,
            GameStart,
        )

    def test_get_game_state(self):
        manager = Manager()
        game = WumpusGame([NAME_USER_1, NAME_USER_2])
        manager.action_data = {"test": "test"}
        self.assertIsInstance(
            manager.get_game_state(game, STATE),
            GameState
        )

    @patch('game.game.WumpusGame.game_over_final_message')
    def test_get_game_state_game_over(self, game_over_mock):
        manager = Manager()
        game = WumpusGame([NAME_USER_1, NAME_USER_2])
        manager.action_data = {"test": "test"}
        manager.get_game_state(game, GAMEOVER_STATE)
        game_over_mock.assert_called_once_with()
        self.assertIsInstance(
            manager.get_game_state(game, GAMEOVER_STATE),
            GameState
        )

    @patch('game.manager.Manager.get_game_state')
    def test_penalize_with_game_over(self, mok_game_set):
        manag = Manager()
        users_names = [NAME_USER_1, NAME_USER_2]
        game = WumpusGame(users_names)
        game_id = "123asd"
        game.game_id = game_id
        game.game_is_active = False
        manag.games[game_id] = game
        manag.penalize(game_id)
        mok_game_set.assert_called_once_with(game, GAMEOVER_STATE)

    @patch('game.manager.Manager.get_game_state')
    def test_penalize_without_game_over(self, mok_game_set):
        manag = Manager()
        users_names = [NAME_USER_1, NAME_USER_2]
        game = WumpusGame(users_names)
        game_id = "123asd"
        game.game_id = game_id
        manag.games[game_id] = game
        manag.penalize(game_id)
        self.assertEqual(manag.action_data, INVALID_PENALIZE)
        mok_game_set.assert_called_once_with(game, TIMEOUT)
