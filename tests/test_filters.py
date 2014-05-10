#!/usr/bin/env python

import unittest
from filtered_websocket.filters.base import FilterBase, FilterMeta


class A(FilterBase):
    class __metaclass__(FilterMeta):
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


if __name__ == '__main__':
    unittest.main()
