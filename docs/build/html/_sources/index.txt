.. filtered_websocket documentation master file, created by
   sphinx-quickstart on Sat Jul 26 20:45:56 2014.

Welcome to filtered_websocket's documentation!
==============================================
Filtered WebSocket is a straight forward module system for composing
complex server's without using callbacks or touching protocol classes.

For instance this module broadcasts messages to all connected users when imported::

    from filtered_websocket.filters.base import WebSocketMessageFilter
    
    
    Class Broadcast(WebSocketMessageFilter):
    @classmethod
    filter(cls, web_socket_instance, data):
        for user_id, user_instance in web_socket_instance.users.items():
            user_instance.sendMessage(bytes(data))



To run the broadcast server written above simply run: ``fws_server -f broadcast``

Contents:

.. toctree::
   :maxdepth: 2

   filter_modules_overview.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

