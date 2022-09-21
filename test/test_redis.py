import unittest
from game.redis import (
    redis_client,
)


class TestRedis(unittest.TestCase):

    def test_create_redis_client(self):
        self.assertIsNotNone(redis_client)
