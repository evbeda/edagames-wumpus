import unittest
from unittest.mock import patch
from edagames_grpc.game_start import GameStart
from edagames_grpc.game_state import GameState
from game.game import WumpusGame
from test.test_game import patched_game
from game.manager import Manager
from parameterized import parameterized
from constants.constants import (
    ABORT,
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
    NAME_USER_2,
    VALID_STATE,
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
        manager = Manager()
        players_names = ['bot1', 'bot2']
        response_manager = manager.create_game(players_names)
        self.assertIsInstance(response_manager, GameStart)
        self.assertNotEqual({}, manager.games)

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
        manag.create_game(users_names)
        key_manag = ""
        for key in manag.games:
            key_manag = key
        with patch('game.manager.Manager.check_game_over', return_value=True):
            manag.penalize(key_manag)
            mok_game_set.assert_called_once_with(manag.games[key_manag], GAMEOVER_STATE)

    @patch('game.manager.Manager.get_game_state')
    def test_penalize_without_game_over(self, mok_game_set):
        manag = Manager()
        users_names = [NAME_USER_1, NAME_USER_2]
        manag.create_game(users_names)
        key_manag = ""
        for key in manag.games:
            key_manag = key
        manag.penalize(key_manag)
        self.assertEqual(manag.action_data, INVALID_PENALIZE)
        mok_game_set.assert_called_once_with(manag.games[key_manag], TIMEOUT)

    @patch.object(Manager, 'find_game')
    @patch.object(Manager, 'get_game_state')
    def test_abort(
        self,
        mock_get_game_state,
        mock_find_game
    ):
        manager = Manager()
        name_users = [NAME_USER_1, NAME_USER_2]
        game = WumpusGame(name_users)
        game_id = 'game_id'
        game.game_id = game_id
        manager.games[game_id] = game
        mock_find_game.return_value = game
        manager.abort(game_id)
        mock_get_game_state.assert_called_once_with(game, ABORT)

    def test_find_game(self):
        game_id_key = 'correct_id'
        manager = Manager()
        game = WumpusGame(['one_player', 'two_player'])
        game.game_id = 'correct_id'
        manager.games['correct_id'] = [game]
        result = manager.find_game(game_id_key)
        self.assertEqual(result, manager.games['correct_id'])

    def test_find_game_failed(self):
        manager = Manager()
        game = WumpusGame(['one_player', 'two_player'])
        game.game_id = 'correct_id'
        manager.games['correct_id'] = [game]
        with self.assertRaises(InvalidData):
            manager.find_game('incorrect_id')

    @patch('game.game.WumpusGame.penalize_player')
    @patch.object(Manager, 'execute_action_manager')
    @patch.object(Manager, 'check_game_over')
    def test_process_request_punible_error_data(
        self,
        mok_penalize_player,
        execute_mock_action,
        mok_check_game_over
    ):
        manag = Manager()
        users_names = [NAME_USER_1, NAME_USER_2]
        game = WumpusGame(users_names)
        game_id = "123asd"
        game.game_id = game_id
        manag.games[game_id] = game
        execute_mock_action.side_effect = InvalidData()
        mok_check_game_over.return_value = False
        manag.process_request(game_id, {})
        mok_penalize_player.assert_called_once()

    @patch('game.game.WumpusGame.penalize_player')
    @patch.object(Manager, 'execute_action_manager')
    @patch.object(Manager, 'check_game_over')
    def test_process_request_punible_error_key(
        self,
        mok_penalize_player,
        execute_mock_action,
        mok_check_game_over
    ):
        manag = Manager()
        users_names = [NAME_USER_1, NAME_USER_2]
        game = WumpusGame(users_names)
        game_id = "123asd"
        game.game_id = game_id
        manag.games[game_id] = game
        execute_mock_action.side_effect = InvalidKey()
        mok_check_game_over.return_value = False
        manag.process_request(game_id, {})
        mok_penalize_player.assert_called_once()

    @patch('game.manager.Manager.get_game_state')
    def test_process_request_without_gameover(self, get_game_mock):
        manag = Manager()
        users_names = [NAME_USER_1, NAME_USER_2]
        game = WumpusGame(users_names)
        game_id = "123asd"
        game.game_id = game_id
        manag.games[game_id] = game
        manag.action_data = {"test": "test"}
        with patch('game.manager.Manager.execute_action_manager', return_value=True):
            with patch('game.manager.Manager.check_game_over', return_value=False):
                manag.process_request(game_id, manag.action_data)
                get_game_mock.assert_called_once_with(game, VALID_STATE)

    @patch('game.manager.Manager.get_game_state')
    def test_process_request_with_gameover(self, get_game_mock):
        manag = Manager()
        users_names = [NAME_USER_1, NAME_USER_2]
        game = WumpusGame(users_names)
        game_id = "123asd"
        game.game_id = game_id
        manag.games[game_id] = game
        manag.action_data = {"test": "test"}
        with patch('game.manager.Manager.execute_action_manager', return_value=True):
            with patch('game.manager.Manager.check_game_over', return_value=True):
                manag.process_request(game_id, manag.action_data)
                get_game_mock.assert_called_once_with(game, GAMEOVER_STATE)

    @parameterized.expand([
        (1.0, 2.0, 1, 2),
        ('1', 1, 1, 1),
    ])
    def test_convertion_index_when_are_no_tints(self, from_row, from_col, expeted_row, expected_col):
        manager = Manager()
        data_message = {
            'from_row': from_row,
            'from_col': from_col,
            'direction': WEST
        }
        expected_result = {
            'from_row': expeted_row,
            'from_col': expected_col,
            'direction': WEST
        }
        result = manager.get_correct_data(data_message, MESSAGE_DATA_KEYS)
        self.assertEqual(result, expected_result)

    @parameterized.expand([
        (0.0, 4.0),
        ('0', '4'),
    ])
    @patch('game.game.WumpusGame.execute_action')
    def test_execute_action_is_coverting_index(self, from_row, from_col, mock_execute_action):
        manager = Manager()
        game = patched_game()
        api_data = dict(
            {
                ACTION: MOVE,
                DATA: {
                    ROW: from_row,
                    COL: from_col,
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

    def test_execute_action_raise_an_error_of_convertion(self):
        manager = Manager()
        game = patched_game()
        api_data = dict(
            {
                ACTION: MOVE,
                DATA: {
                    ROW: 'a',
                    COL: 'b',
                    DIRECTION_MESSAGE: NORTH
                }
            }
        )
        with self.assertRaises(InvalidData):
            manager.execute_action_manager(game, api_data)
