"""
FilterBase and FilterMeta allow for the simple creation of a filter chains.
Any class that inherits from a child of FilterBase and FilterMeta
will have its filter method called upon run being executed from its parent class.

Ex:

>>> class A(FilterBase):
>>>     class __metaclass__(FilterMeta):
>>>         pass

>>> class B(A):
>>>     @classmethod
>>>     def filter(cls, web_socket_instance, data):
>>>        print("foo")

>>> class C(A):
>>>     @classmethod
>>>     def filter(cls, web_socket_instance, data):
>>>         print("bar")

>>> A.run(web_socket_instance)
foo
bar

"""

from __future__ import absolute_import


class FilterBase(object):
    @classmethod
    def run(cls, web_socket_instance, data=None):
        for filter in cls._filters:
            filter.filter(web_socket_instance, data)

    @classmethod
    def filter(cls, web_socket_instance, data=None):
        raise NotImplementedError


class FilterMeta(type):
    def __init__(self, name, _type, other):
        if self.__base__ is not FilterBase:
            self.__class__._filters.append(self)
        else:
            self.__class__._filters = []


def generate_filter_chain(class_name):
    """
    Returns a new FilterChain base class of the given name.
    equivalant to: class class_name(FilterBase, metaclass=FilterMeta):
    """
    return FilterMeta(class_name, (FilterBase,), {})

WebSocketDataFilter = generate_filter_chain("WebSocketDataFilter")
WebSocketMessageFilter = generate_filter_chain("WebSocketMessageFilter")
WebSocketDisconnectFilter = generate_filter_chain("WebSocketDisconnectFilter")
WebSocketConsumerFilter = generate_filter_chain("WebSocketConsumerFilter")
