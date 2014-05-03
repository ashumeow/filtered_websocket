#!/usr/bin/env python

"""
Importing the broadcast_message_filter module creates a simple chat server.
"""

import sys
sys.path.append("../../")

from filtered_websocket.server import * # NOQA
from filtered_websocket.filters import broadcast_message_filter # NOQA


parser = default_parser()
build_reactor(parser.parse_args(sys.argv[1:]))
reactor.run()
