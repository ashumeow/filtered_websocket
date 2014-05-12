import sys
from base import StorageObjectPubSubFilter


class BroadcastMessageFilter(StorageObjectPubSubFilter):

    @classmethod
    def filter(cls, web_socket_instance, data):
        sys.stdout.writelines(
            "--PUBSUB--\n%s\n" % (data)
        )
        sys.stdout.flush()
