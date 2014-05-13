from filters.base import StorageObjectPubSubFilter
from base import BasePubSubListener


class RedisPubSubListener(BasePubSubListener):

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
