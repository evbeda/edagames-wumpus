from game.grpc_interface import Interface
from unittest import IsolatedAsyncioTestCase
from game.manager import Manager
from unittest.mock import patch


class TestInterface(IsolatedAsyncioTestCase):

    @patch.object(Manager, 'create_game')
    async def test_create_game(self, mock_method):
        interface = Interface()
        names = ['name1', 'name2']
        await interface.create_game(names)
        mock_method.assert_called_once_with(names)

    @patch.object(Manager, 'penalize')
    async def test_penalize(self, mock_method):
        interface = Interface()
        id_game = 'game_id'
        await interface.penalize(id_game)
        mock_method.assert_called_once_with(id_game)

    @patch.object(Manager, 'abort')
    async def test_end_game(self, mock_method):
        interface = Interface()
        id_game = 'game_id'
        await interface.end_game(id_game)
        mock_method.assert_called_once_with(id_game)

    @patch.object(Manager, 'process_request')
    async def test_process_request(self, mock_method):
        interface = Interface()
        id_game = 'one_id'
        dictio = {'key1': 'value1'}
        await interface.execute_action(id_game, dictio)
        mock_method.assert_called_once_with(id_game, dictio)
