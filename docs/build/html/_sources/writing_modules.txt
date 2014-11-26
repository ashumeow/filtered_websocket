Writing Modules
================

Introduction
_____________

In Filtered WebSocket, instead of using callbacks, new behaviors are added by writing modules which inherit from base WebSocketFilter types.  Each base filter class represents an entry point into a chain of modules which will run, in the order in which they were added, whenever some event happens.

.. automodule:: filtered_websocket.filters.base

Each filter has access to a server instance with a dictionary of user ids mapped to user objects, a storage object, and an optional token object for storing credentials.  It also receives payload data in the form of a bytearray().

Filter Module Types
--------------------

There are four filter chains, each corresponding to a callback.

.. autoclass:: filtered_websocket.filters.base.WebSocketDataFilter
.. autoclass:: filtered_websocket.filters.base.WebSocketMessageFilter
.. autoclass:: filtered_websocket.filters.base.WebSocketDisconnectFilter
.. autoclass:: filtered_websocket.filters.base.WebSocketConsumerFilter


Example Module
---------------

To write a module that responds to some sort of event just make it a subclass of the corresponding parent and override "filter" as either a classmethod or a static method.  Let's write a rawdata module that responds to my name::

    # Saved as hi_morgan.py
    class HiMorgan(WebSocketDataFilter):
        @classmethod
        filter(cls, web_socket_instance, data):
            payload = bytes(data)
            if payload.lower().strip() == b'morgan':
                print('Hi Mrrrgn!')
   

To inject the module into the server import it via the '-f' option::

    $ fws_server -f hi_morgan

    $ echo "Morgan" | nc localhost 9000
    $ Hi Mrrrgn!

Building Pipelines via Data Mutability & Run Order
---------------------------------------------------

Filter modules run in the order that they are imported and are passed mutable object refernces, meaning, they may be composed into pipelines.  The filter below pops the last character off of any data sent, when combined with a default filter module which prints client messages it demonstrates that data has indeed been manipulated en route::

    # Saved as popchar.py
    class PopChar(WebSocketMessageFilter):
        @classmethod
        filter(cls, web_socket_instance, data):
            data.pop()  # remove last character from the bytearray

    # Server console
    $ fws_server -f popchar filtered_websocket.filters.stdout_messages

    # From a browser JS console
    >>> var ws = new WebSocket("ws://localhost:9000");
    >>> ws.send("Test");

    # Server console
    $ Tes

Now, if we reverse the order of the modules the data is printed before the character is popped::
    
    # Server console
    $ fws_server -f filtered_websocket.filters.stdout_messages popchar

    # From a browser JS console
    >>> var ws = new WebSocket("ws://localhost:9000");
    >>> ws.send("Test");

    # Server console
    $ Test

Additional Examples
--------------------

For additional module examples please see the default modules.
