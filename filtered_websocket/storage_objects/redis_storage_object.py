import redis
import redis_collections

from filters.base import StorageObjectPubSubFilter
from default_storage_object import BasePubSubStorageObject


def redis_parser(parser):
    parser.add_argument(
        "--redis",
        help="Use redis as a storage object.",
        action="store_true"
    )
    parser.add_argument(
        "--redis_host",
        default="localhost"
    )
    parser.add_argument(
        "--redis_port",
        type=int,
        default=6379
    )
    parser.add_argument(
        "--redis_channels",
        help="pubsub channels to subscribe to.",
        nargs="*"
    )
    parser.add_argument(
        "--redis_key",
        help="A key prefix.",
        default="my_app"
    )
    return parser


class RedisStorageObject(BasePubSubStorageObject):

    def __init__(self, *args, **kwargs):
        host = kwargs.get("host")
        port = kwargs.get("port")
        key = kwargs.get("key")
        self.redis = redis.Redis(host=host, port=port)
        self.storage = redis_collections.Dict(key=key, redis=self.redis)

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

    def publish(self, channel, data):
        self.redis.publish(channel, data)


class RedisPubSubListener(object):

    kill_channel = "__KILL__"

    def __init__(self, redis_client, channels=None):
        self.redis_client = redis_client
        if channels is None:
            channels = ["global"]
        # The __KILL__ channel is used to coerce the thread
        # to finish in kill()
        channels += [self.kill_channel]
        self.pubsub = self.redis_client.pubsub()
        self.pubsub.subscribe(channels)
        self.__KILL__ = False

    def kill(self):
        self.__KILL__ = True
        self.redis_client.publish(self.kill_channel, "#YOLO")

    def listen(self, web_socket_instance):
        for data in self.pubsub.listen():
            StorageObjectPubSubFilter.run(web_socket_instance, data)
            if self.__KILL__ is True:
                self.pubsub.unsubscribe()
                break
