Filtered WebSocket
===================

A straight forward framework for implementing websocket servers via filter chains.

*features:*

- Supports SSL
- Scales horizontally via remote backend storage (redis)
- Supports token based auth


New behaviors are added by simply importing filter modules.
    
    from filtered_websocket.filters import stdout_rawdata # Adds logging to a server
    from filtered_websocket.filters import broadcast_message_filter # Broadcasts messages to all connected clients
    
###### Create New Filters

Filter chains are implemented like so:

    >>> class A(FilterBase):
    >>>     class __metaclass__(FilterMeta):
    >>>         pass
    
    >>> Class B(A):
    >>>     @classmethod
    >>>     def filter(cls, web_socket_instance):
    >>>        print("foo")
    
    >>> Class C(A):
    >>>     @classmethod
    >>>     def filter(cls, web_socket_instance):
    >>>         print("bar")
    
    >>> A.run(web_socket_instance)
    foo
    bar

In filtered_websocket.server each server event has a corresponding filter chain, like the one shown above:

    WebSocketDataFilter # Will run against any data received event
    WebSocketMessageFilter # Will run against any valid message frames
    WebSocketDisconnectFilter # Will run anytime a client disconnects

To create a new filter simply inherit from one of the base filter classes.

*example: stdout_rawdata.py*

    import sys
    from base import WebSocketDataFilter
    
    
    class BroadcastMessageFilter(WebSocketDataFilter):
        """
        Runs on each dataReceived event.
        """
        @classmethod
        def filter(cls, web_socket_instance, data):
            sys.stdout.writelines("--RAWDATA--\n%s\n" % data)
            sys.stdout.flush()

*example: chat_server.py*

    from filtered_websocket.server import * 
    from filtered_websocket.filters import broadcast_message_filter 


    parser = default_parser()
    build_reactor(parser.parse_args(sys.argv[1:]))
    reactor.run()

*chat_server.py output*

    ./chat_server.py --help
    usage: chat_server.py [-h] [-p PORT] [-key KEY] [-cert CERT] [-token TOKEN]

    optional arguments:
      -h, --help            show this help message and exit
      -p PORT, --port PORT  The listening port.
      -key KEY              A key file (ssl).
      -cert CERT            A certificate file (ssl).
      -token TOKEN          Set a default token.


Redis back end support allows shared storage with other applications.

    extra = {
        "storage_object": RedisStorageObject(
            host=options.redis_host,
            port=options.redis_port,
            key=options.redis_key
        )
    }
    build_reactor(options, **extra)

