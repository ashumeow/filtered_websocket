#!/usr/bin/env python

import sys
sys.path.append("../../")

from twisted.internet import reactor

from filtered_websocket.server import (
    default_parser,
    build_reactor
)
from filtered_websocket.filters import token_broadcast_filters # NOQA
from filtered_websocket.storage_objects.redis_storage_object import (
    RedisStorageObject,
    redis_subparser
)


parser = default_parser()
parser = redis_subparser(parser)
options = parser.parse_args(sys.argv[1:])

extra = {
    "storage_object": RedisStorageObject(
        host=options.redis_host,
        port=options.redis_port,
        key=options.redis_key
    )
}

build_reactor(options, **extra)
reactor.run()
