from edagames_grpc.server import ServerInterface
from edagames_grpc.game_state import GameState
from edagames_grpc.game_start import GameStart

from game.manager import Manager

from typing import List, Dict


MANAGER = Manager()


class Interface(ServerInterface):

    async def create_game(self, players: List[str]) -> GameStart:
        return MANAGER.create_game(players)

    async def penalize(self, game_id: str) -> GameState:
        return MANAGER.penalize(game_id)

    async def end_game(self, game_id: str) -> GameState:
        return MANAGER.abort(game_id)

    async def execute_action(self, game_id: str, game_data: Dict) -> GameState:
        return MANAGER.process_request(game_id, game_data)
