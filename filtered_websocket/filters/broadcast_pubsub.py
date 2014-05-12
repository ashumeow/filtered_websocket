from base import StorageObjectPubSubFilter


class BroadcastMessageFilter(StorageObjectPubSubFilter):
    """
    Will broadcast all pubsub events to connected websocket clients.
    """

    @classmethod
    def filter(cls, web_socket_instance, data):
        for _id, user in web_socket_instance.users.items():
            user.sendMessage(data.get("data"))
