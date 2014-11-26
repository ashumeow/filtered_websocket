A Closer Look At Redis Integration
----------------------------------

Along with filter modules, filtered_websocket also supports pluggable back end storage via the StorageObject and PubSubStorageObject interfaces.  To use redis as a distributed storage object and message broker simply set the environment variable "STORAGE_OBJECT_MODULE"

``export STORAGE_OBJECT_MODULE=filtered_websocket.storage_objects.redis``

If you look at fws_server you'll now notice some new options for managing your redis connection::

    fws_server -h
    usage: fws_server [-h] [-p PORT] [-c CONFIG] [-f [FILTERS [FILTERS ...]]]
                      [-key KEY] [-cert CERT] [--redis_host REDIS_HOST]
                      [--redis_port REDIS_PORT]
                      [--redis_channels [REDIS_CHANNELS [REDIS_CHANNELS ...]]]
                      [--redis_key REDIS_KEY]

    optional arguments:
      -h, --help            show this help message and exit
      -p PORT, --port PORT  The listening port.
      -c CONFIG, --config CONFIG
                            A JSON config file.
      -f [FILTERS [FILTERS ...]], --filters [FILTERS [FILTERS ...]]
                            Filters to import at runtime.
      -key KEY              A key file (ssl).
      -cert CERT            A certificate file (ssl).
      --redis_host REDIS_HOST
      --redis_port REDIS_PORT
      --redis_channels [REDIS_CHANNELS [REDIS_CHANNELS ...]]
                            pubsub channels to subscribe to.
      --redis_key REDIS_KEY
                            A key prefix.


Supported Default Modules
-------------------------

By default the redis storage object listens to a channel called "global" and will attach any messages it receives to the server instances's queue.  As such messages from redis may be handled by the consumer filter.  As an example examine the default stdout_pubsub filter module::

``fws_server -f filtered_websocket.filters.stdout_pubsub``

.. autoclass:: filtered_websocket.filters.stdout_pubsub.StdoutPubSubFilter

Importing the stdout_pubsub filter will print all redis messages captured by the server to your console::

    import redis
    redis_client = redis.Redis()
    redis_client.publish("global", "hello from the server!")

To send redis messages to connected clients use the ``broadcast_pubsub`` filter:

``fws_sever -f filtered_websocket.filters.broadcast_pubsub``

.. autoclass:: filtered_websocket.filters.broadcast_pubsub.BroadcastPubSubFilter


Using The Redis Storage Object
------------------------------
Inside your modules any data written to ``web_socket_instance.storage_object`` will go to redis.  The storage object interface is defined as::

    web_socket_instance.storage_object.get(key) # Try to grab some data from redis
    web_socket_instance.storage_object.add(key, value) # Add some data to redis
    web_socket_instance.remove(key, value) # delete something in a fashion akin to storage_object[key].remove(value)

Writing Modules For Redis PubSub
--------------------------------

All data received from pubsub subscriptions will be attached to the server's queue and later consumed.  So, modules
which wish to interact with these events should inherit from:

.. autoclass:: filtered_websocket.filters.base.WebSocketConsumerFilter
