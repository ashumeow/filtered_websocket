#!/usr/bin/env python

import unittest
from filtered_websocket.server import FilteredWebSocket


class FilteredWebSocketTest(unittest.TestCase):
    def test_data_structures(self):
        """
        Verify that the users, token, queue, and storage_object
        are available.
        """
        protocol = FilteredWebSocket(storage_object=True, token=True)
        self.assertIsNotNone(protocol.storage_object)
        self.assertIsNotNone(protocol.token)
        self.assertIsNotNone(protocol.users)
        self.assertIsNotNone(protocol.queue)


if __name__ == '__main__':
    unittest.main()
