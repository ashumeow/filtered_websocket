from __future__ import absolute_import

import sys
from .base import WebSocketConsumerFilter


class StdoutPubSubFilter(WebSocketConsumerFilter):
    """
    Print any consumed queue data to the server console's stdout.
    """
    @classmethod
    def filter(cls, web_socket_instance, data):
        sys.stdout.writelines(
            "--PUBSUB--\n%s\n" % (data)
        )
        sys.stdout.flush()
