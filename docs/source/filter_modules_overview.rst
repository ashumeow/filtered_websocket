Filter Module Overview
================

Introduction:

In Filtered WebSocket instead of using callbacks new behaviors are added by writing modules which inherit from base filter classes.  Each base class represents an entry point into a chain of modules which will run, in the order in which they were added, whenever some event happens.

.. automodule:: filtered_websocket.filters.base

There are four filter chains, each corresponding to a callback.

.. autoclass:: filtered_websocket.filters.base.WebSocketDataFilter
.. autoclass:: filtered_websocket.filters.base.WebSocketMessageFilter
.. autoclass:: filtered_websocket.filters.base.WebSocketDisconnectFilter
.. autoclass:: filtered_websocket.filters.base.WebSocketConsumerFilter
