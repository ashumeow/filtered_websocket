Filtered WebSocket
===================

Filtered WebSocket is a straight forward framework for implementing websocket servers which draws inspiration from UNIX process pipelines.  It's a metaphor for:

    cat server_event | behavior_a | behavior_b | ...

Server event handlers are encapsulated within filters such that building elaborate behaviors is as easy as importing new modules.  Imported filters automatically add themselves to an appropriate filter chain (pipeline).


*features:*

- Supports SSL
- Scales horizontally via remote backend storage (redis) and pubsub
- Supports token based auth


New behaviors are added by simply importing filter modules.
    
    from filtered_websocket.filters import stdout_rawdata # Adds logging to a server
    from filtered_websocket.filters import broadcast_messages # Broadcasts messages to all connected clients

###### Install 
    pip install filtered_websocket

###### Run The Server With Default Filters (stdout_messages and broadcast_messages_by_token)
    python -m filtered_websocket.server
   
###### Build a unique server from the CLI using filters as arguments

    # It should generally be un-necessary to touch server.py unless you want to write your own storage back ends or pubsub listeners.
    # Instead write filter modules and import them at runtime like so:
    # The server below will broadcast messages to all connected clients and print all
    # data passing through it to stdout. 
    python -m filtered_websocket.server -f "filtered_websocket.filters.broadcast_messages" "filtered_websocket.filters.stdout_rawdata"

###### Define a unique server via a json config file
    # config.json
    {
        "port": "9000",
        "flags": ["redis"],
        "filters": ["filtered_websocket.filters.broadcast_messages_by_token", "filtered_websocket.filters.stdout_messages"]
    }

    # Passing it in creates a broadcast by token server with backed by redis which prints all messages to stdout
    python -m filtered_websocket.server -c config.json

###### Create New Filters

Filter chains are implemented like so:

    >>> class AFilter(FilterMeta)
    >>>     pass
    >>>
    >>> @add_metaclass(AFilter)
    >>> class A(FilterBase):
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

In filtered_websocket.server each server event has a corresponding base filter class, like the class 'A' shown above:

    WebSocketDataFilter # Will run against any data received event
    WebSocketMessageFilter # Will run against any valid message frames
    WebSocketDisconnectFilter # Will run anytime a client disconnects
    WebSocketConsumerFilter # Will run against any data placed into a web socket instance's queue

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

*example: chat_server*

    # Just import the filters you'd like at runtime instead of touching server.py
    python -m filtered_websocket.server -f "filtered_websocket.filters.broadcast_messages"

Redis back end support allows shared storage with other applications.

    extra = {
        "storage_object": RedisStorageObject(
            host=options.redis_host,
            port=options.redis_port,
            key=options.redis_key
        )
    }
    build_reactor(options, **extra)

The redis pubsub_listener places all redis pubsub events in a queue where it may be handled by WebSocketConsumerFilter filters.
    
    redis_storage_object = RedisStorageObject(
        host=options.redis_host,
        port=options.redis_port,
        key=options.redis_key
    )
    redis_pubsub = RedisPubSubListener(
        redis_storage_object.redis,
        options.redis_channels
    )
    # Build our server reactor.
    web_socket_instance = build_reactor(
        options,
        storage_object=redis_storage_object,
        pubsub_listener=redis_pubsub
    )
     
