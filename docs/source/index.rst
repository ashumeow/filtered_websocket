.. filtered_websocket documentation master file, created by
   sphinx-quickstart on Sat Jul 26 20:45:56 2014.

Welcome to filtered_websocket's documentation!
==============================================

Filtered WebSocket is a straight forward server framework which allows you to compose
complex behaviors without using callbacks or subclassing any protocols.
It also features redis integration for remote storage and message passing via pubsub.

Install
-------

``pip install filtered_websocket`` or clone the repository and run ``python setup.py install``

Getting Started
---------------

After installing filtered_websocket you'll have access to the server launcher via ``fws_server``.
Running ``fws_server -h`` will give you a list of configuration options while simply running ``fws_server``
will start a server running the default broadcast_messages and stdout_messages modules on port 9000.

filtered_websocket is bundled with several useful modules which may be attached to a server via the '-f' option like so::

    # This will start a server which prints rawdata and broadcasts messages to users who have set a "token"
    >>> fws_server -f filtered_websocket.filters.stdout_rawdata filtered_websocket.filters.broadcast_messages_by_token

Using Redis
-----------

Redis integration is activated by setting an environment variable ``STORAGE_OBJECT_MODULE`` to ``filtered_websocket.storage_objects.redis``.
When the redis storage object is activated ``fws_server -h`` will display new argument options for configuring your redis instance connection and channel subscriptions.

The following would start a server which broadcasts messages received from a redis channel named global to all connected clients::

    >>> export STORAGE_OBJECT_MODULE="filtered_websocket.storage_objects.redis"
    >>> fws_server -f filtered_websocket.filters.broadcast_pubsub

This message, published via a redis client, connected to the same redis instance, would be sent to all connected WebSocket clients::

    >>> import redis
    >>> r = redis.Redis() # connections to localhost on default port
    >>> r.publish("global", "hello from the server!") # Connected WebSocket clients receive this message

To start a server which broadcasts messages both between clients and from remote, server side, processes to clients::

    >>> export STORAGE_OBJECT_MODULE="filtered_websocket.storage_objects.redis"
    >>> fws_server -f filtered_websocket.filters.broadcast_messages filtered_websocket.filters.broadcast_pubsub

Custom Modules
---------------

Writing servers with filtered_websocket is extremely terse.  Here is an entire broadcast/chat server::
    
    # saved as broadcast.py
    Class Broadcast(WebSocketMessageFilter):
    @classmethod
    filter(cls, web_socket_instance, data):
        for user_id, user_instance in web_socket_instance.users.items():
            user_instance.sendMessage(bytes(data))



To run the broadcast server written above simply run: ``fws_server -f broadcast``

Configuration Files
-------------------

Any argument from the help menu may be used to create a json formatted config file.  Simply use the long form (-- prefixed) option names as keys and pass in arguments as values.  Any filters specified should be added within a list::

    # config.json
    {
        "port": "9999",
        "filters": ["filtered_websocket.filters.broadcast_messages_by_token", "filtered_websocket.filters.stdout_messages"]
    }

    # Passing it in creates a broadcast by token server which prints all messages to stdout
    fws_server -c config.json


Contents:

.. toctree::
   :maxdepth: 2

   default_modules.rst
   writing_modules.rst
   redis_integration.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

