Default Modules
----------------

Any or all of these may be used to compose a custom server via: ``fws_server -f``

.. autoclass:: filtered_websocket.filters.broadcast_messages.BroadcastMessagesFilter
.. autoclass:: filtered_websocket.filters.broadcast_messages_by_token.TokenMessageFilter
.. autoclass:: filtered_websocket.filters.broadcast_messages_by_token.TokenDisconnectFilter
.. autoclass:: filtered_websocket.filters.broadcast_pubsub.BroadcastPubSubFilter
.. autoclass:: filtered_websocket.filters.stdout_rawdata.StdoutRawDataFilter
.. autoclass:: filtered_websocket.filters.stdout_messages.StdoutMessageFilter
.. autoclass:: filtered_websocket.filters.stdout_pubsub.StdoutPubSubFilter
