Filtered WebSocket
===================

A straight forward framework for implementing websocket servers via filter chains.

*features:*

- Supports SSL
- Supports Redis for backend session storage
- Scales horizontally via remote backend storage
- Supports token based auth


Complex behaviors are added by simply importing filter modules.
    
    from filtered_websocket.filters import stdout_rawdata # Adds logging to a server
    from filtered_websocket.filters import broadcast_message_filter # Broadcasts messages to all connected clients
    
and all data sent to the server will print via stdin.

###### Create New Filters

To create a new filter simply inherit from one of the base filter classes:

    WebSocketDataFilter # Will run against any data received event
    WebSocketMessageFilter # Will run against any valid message frames
    WebSocketDisconnectFilter # Will run anytime a client disconnects
    
*example: a broadcast server*

    from filtered_websocket.server import * 
    from filtered_websocket.filters import broadcast_message_filter 


    parser = default_parser()
    build_reactor(parser.parse_args(sys.argv[1:]))
    reactor.run()
