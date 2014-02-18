#!/usr/bin/env python2
import unittest

from zmq_avro import client, server


class TestZMQAvro(unittest.TestCase):
    port = 12345
    host = '127.0.0.1'

    def setUp(self):
        # the server should be started first
        self.client = client.Client(self.host, self.port)
        self.server = server.Server(self.host, self.port)
        self.server.start()

    def tearDown(self):
        self.client.close()
        self.server.close()

    def test_send_message(self):
        # make sure server receives whatever json client sends
        # make sure non-json messages or json messages with incorrect scheme
        # are handled properly
        self.assertIsNone(self.server._last_msg)

        msg = 'ahoj'
        self.client.send(msg)
        self.assertEqual(self.server._last_msg, msg)

    def test_message_logged(self):
        # make sure messages are logged on the server for auditing
        pass

    def test_valid_message(self):
        # make sure only authenticated messages are accepted
        pass

    def test_invalid_message(self):
        # make sure unauthenticated messages are not accepted
        # 1) signed with a wrong key
        # 2) missing signature
        # 3) non-existing key
        pass


if __name__ == '__main__':
    unittest.main()
