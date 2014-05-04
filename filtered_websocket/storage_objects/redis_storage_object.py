import redis
import redis_collections

from default_storage_object import BaseStorageObject


def redis_subparser(parser):
    sub_parsers = parser.add_subparsers()
    redis_parser = sub_parsers.add_parser(
        "redis",
        help="Use redis to back the server's storage object."
    )
    redis_parser.add_argument(
        "-redis_host",
        default="localhost"
    )
    redis_parser.add_argument(
        "-redis_port",
        type=int,
        default=6379
    )
    redis_parser.add_argument(
        "-redis_key",
        help="A key prefix.",
        default="app_key"
    )


class RedisStorageObject(BaseStorageObject):

    def __init__(self, *args, **kwargs):
        host = kwargs.get("host", "localhost")
        port = kwargs.get("port", 6379)
        key = kwargs.get("key", "my_app")
        self.storage = redis_collections.Dict(key=key, redis=redis.Redis(host=host, port=port))

    def __getitem__(self, item):
        return self.storage.get(item)

    def add(self, key, value):
        current = self.storage.get(key)
        if current is None:
            current = set()
        current.add(value)
        self.storage[key] = current

    def remove(self, key, item):
        current = self.storage.get(key)
        if current is not None:
            current.remove(item)
            self.storage[key] = current
