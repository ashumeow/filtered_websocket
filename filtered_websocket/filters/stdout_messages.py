from __future__ import absolute_import

import sys
from .base import WebSocketMessageFilter


class StdoutMessageFilter(WebSocketMessageFilter):
    """
    Print any client messages received to the server console's stdout.
    """
    @classmethod
    def filter(cls, web_socket_instance, msg):
        sys.stdout.writelines(
            "--MESSAGE--\n%s => %s\n" % (web_socket_instance.id, msg)
        )
        sys.stdout.flush()
