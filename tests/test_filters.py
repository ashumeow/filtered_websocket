#!/usr/bin/env python

from __future__ import absolute_import

import unittest
from six import add_metaclass

from filtered_websocket.filters.base import (
    FilterBase,
    FilterMeta,
    WebSocketDataFilter,
    WebSocketMessageFilter,
    WebSocketDisconnectFilter,
)
from filtered_websocket.server import FilteredWebSocket


@add_metaclass(FilterMeta)
class A(FilterBase):
    pass


class B(A):
    @classmethod
    def filter(cls, data_object, extra=None):
        data_object.append("foo")


class C(A):
    @classmethod
    def filter(cls, data_object, extra=None):
        data_object.append("bar")


class FilterBaseTestCase(unittest.TestCase):

    def test_filter_chain(self):
        self.assertEqual(A._filters, [B, C])

    def test_run(self):
        data_object = []
        A.run(data_object)
        self.assertEqual(data_object, ["foo", "bar"])


class FilterModulesTestCase(unittest.TestCase):
    class TestDataFilter(WebSocketDataFilter):
        @classmethod
        def filter(cls, wsi, data):
            # Attach some value to the web socket instance storage object
            # to indicate success.
            wsi.storage_object["data_filter"] = data

    class TestMessageFilter(WebSocketMessageFilter):
        @classmethod
        def filter(cls, wsi, data):
            wsi.storage_object["message_filter"] = data

    class TestDisconnectFilter(WebSocketDisconnectFilter):
        @classmethod
        def filter(cls, wsi, data):
            wsi.storage_object["disconnect_filter"] = True

    def setUp(self):
        self.protocol = FilteredWebSocket(storage_object={}, token=None)

        # Values passed into filters to prove that they are receiving data
        self.DATA_FILTER_DATA = "data!"
        self.MESSAGE_FILTER_DATA = "message!"

    def test_data_filter(self):
        self.protocol.dataReceived(self.DATA_FILTER_DATA)
        self.assertEquals(
            self.protocol.storage_object.get("data_filter"),
            self.DATA_FILTER_DATA
        )

    def test_message_filter(self):
        self.protocol.onMessage(self.MESSAGE_FILTER_DATA)
        self.assertEquals(
            self.protocol.storage_object.get("message_filter"),
            self.MESSAGE_FILTER_DATA
        )

    def test_disconnect_filter(self):
        self.protocol.onDisconnect()
        # The disconnect doesn't receive data so we just set it's
        # storage_object key to True in the test filter.
        self.assertTrue(self.protocol.storage_object.get("disconnect_filter"))


if __name__ == '__main__':
    unittest.main()
