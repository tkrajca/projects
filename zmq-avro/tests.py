#!/usr/bin/env python2
import unittest

from zmq_avro import client, server


class TestZMQAvro(unittest.TestCase):
    def setUp(self):
        self.client = client
        self.server = server

    def test_send_message(self):
        # make sure server receives whatever json client sent
        """
        self.seq.sort()
        self.assertEqual(self.seq, list(range(10)))

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1,2,3))
        """
        pass

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
