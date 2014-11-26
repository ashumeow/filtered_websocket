"""
FilterBase and FilterMeta allow for the simple creation of a filter chains.
Any class that inherits from a child of FilterBase and FilterMeta
will have its filter method called upon run being executed from its parent class.
Here class A constructs a new filter chain, which B and C become members of.

>>> class A(FilterBase, metaclass=FilterMeta)
>>>         pass
>>>
>>> class B(A):
>>>     @classmethod
>>>     def filter(cls, web_socket_instance, data):
>>>        print("foo")
>>>
>>> class C(A):
>>>     @classmethod
>>>     def filter(cls, web_socket_instance, data):
>>>         print("bar")
>>>
>>> A.run(web_socket_instance, None)
foo
bar

"""

from __future__ import absolute_import

from six import add_metaclass


class FilterBase(object):
    @classmethod
    def run(cls, web_socket_instance, data=None):
        for filter in cls._filters:
            filter.filter(web_socket_instance, data)

    @classmethod
    def filter(cls, web_socket_instance, data=None):
        raise NotImplementedError


class FilterMeta(type):
    def __init__(self, name, type, other):
        if self.__base__ is not FilterBase:
            self.__class__._filters.append(self)
        else:
            self.__class__._filters = []


class DataFilterMeta(FilterMeta):
    pass


@add_metaclass(DataFilterMeta)
class WebSocketDataFilter(FilterBase):
    """
    Runs whenever a web socket server instance receives any data from a client.
    """
    pass


class MessageFilterMeta(FilterMeta):
    pass


@add_metaclass(MessageFilterMeta)
class WebSocketMessageFilter(FilterBase):
    """
    Runs whenever a web socket server instance receives a full data frame.
    """
    pass


class DisconnectFilterMeta(FilterMeta):
    pass


@add_metaclass(DisconnectFilterMeta)
class WebSocketDisconnectFilter(FilterBase):
    """
    Runs whenever a user disconnects from a web socket server instance
    (passes in no data).
    """
    pass


class ConsumerFilterMeta(FilterMeta):
    pass


@add_metaclass(ConsumerFilterMeta)
class WebSocketConsumerFilter(FilterBase):
    """
    Runs whenever data is popped off of a web socket server instance's queue.
    """
    pass
