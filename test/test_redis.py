import unittest
from game.redis import (
    create_redis
)


class TestRedis(unittest.TestCase):

    def test_create_redir(self):
        self.assertEqual(True, create_redis())
