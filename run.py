import asyncio
import os

from game.grpc_interface import Interface

WUMPUS_GRPC_PORT = int(os.environ.get('WUMPUS_GRPC_PORT', '50052'))


if __name__ == '__main__':
    s = Interface(port=WUMPUS_GRPC_PORT)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(s.start_and_wait())
    loop.run_forever()
