#!/usr/bin/env python

import unittest
from filtered_websocket.config_deserializer import config_deserializer


class ConfigDeserializerTestCase(unittest.TestCase):
    def setUp(self):
        self.config_file = "/tmp/config_deserializer_test_case_test_file.json"
        with open(self.config_file, "w") as config:
            config.write(
                "{\"port\": \"2718\", \"flags\": [\"flag_one\", \"flag_two\"]"
                ", \"filters\": [\"a\", \"b\", \"c\"]}"
            )

    def test_deserialize(self):
        deserialized_config = config_deserializer(self.config_file)
        expected_ops = [
            "--port",
            "2718",
            "--flag_one",
            "--flag_two",
            "--filters",
            "a",
            "b",
            "c",
        ]

        for opt in expected_ops:
            self.assertIn(opt, deserialized_config)

if __name__ == '__main__':
    unittest.main()
