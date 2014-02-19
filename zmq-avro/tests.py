#!/usr/bin/env python2
import unittest
import time

from zmq_avro import client, server, models

from contextlib import closing


class TestZMQAvro(unittest.TestCase):
    port = 12345
    host = '127.0.0.1'
    msg1 = {
        'timestamp': int(time.time()),
        'indicator': 'power',
        'value': 4
    }
    msg2 = {
        'timestamp': int(time.time()),
        'indicator': 'failure',
        'value': 5
    }

    def setUp(self):
        # the server should be started first
        self.client = client.Client(self.host, self.port)
        self.server = server.Server(self.host, self.port)
        self.server.start()

    def tearDown(self):
        self.client.close()
        self.server.close()

    def _audit_log_length(self):
        with closing(self.server.Session()) as session:
            count = len(session.query(models.Audit).all())
        return count

    def _clean_msg(self, msg):
        msg2 = msg.copy()
        if 'signature' in msg2:
            del msg2['signature']
        if 'issuedAt' in msg2:
            del msg2['issuedAt']
        msg2['value'] = int(msg2['value'])
        return msg2

    def test_send_message(self):
        # make sure the server receives whatever client sends (in json)
        # providing it has a valid signature
        # assume valid signature (invalid signature is tested elsewhere)
        # TODO: make sure non-json messages or json messages with incorrect
        # scheme are handled properly

        # empty
        self.assertIsNone(self.server._last_msg)

        # valid
        self.client.send(self.msg1, models.KEY, models.SECRET)
        self.assertEqual(self._clean_msg(self.server._last_msg), self.msg1)

        # invalid
        self.client.send(self.msg2, '123', '456')
        self.assertNotEqual(self._clean_msg(self.server._last_msg), self.msg2)
        self.assertEqual(self._clean_msg(self.server._last_msg), self.msg1)

        # valid
        self.client.send(self.msg2, models.KEY, models.SECRET)
        self.assertEqual(self._clean_msg(self.server._last_msg), self.msg2)

    def test_message_logged(self):
        # make sure messages are logged on the server for auditing
        # valid messages are logged, invalid messages are dropped
        self.assertEqual(self._audit_log_length(), 0)

        self.client.send(self.msg1, models.KEY, models.SECRET)
        self.assertEqual(self._audit_log_length(), 1)

        self.client.send(self.msg2, '123', '456')
        self.assertEqual(self._audit_log_length(), 1)

        self.client.send(self.msg2, models.KEY, models.SECRET)
        self.assertEqual(self._audit_log_length(), 2)


if __name__ == '__main__':
    unittest.main()
