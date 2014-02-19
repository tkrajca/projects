#!/usr/bin/env python2

import sys
import logging
import zmq
import time
import StringIO
import os

import avro.schema
from avro.datafile import DataFileWriter
from avro.io import DatumWriter

from contextlib import closing

from zmq_avro.utils import sign
from zmq_avro.models import KEY, SECRET


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('zmq_avro.client')


class Client(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        logger.info("Connecting to {0}:{1}".format(self.host, self.port))
        # let's keep a persistent connection for each client
        self.socket.connect("tcp://{0}:{1}".format(self.host, self.port))
        self.schema = avro.schema.parse(open(os.path.join(
            os.path.dirname(__file__), "example.avsc")).read())

    def send(self, msg, key, secret):
        assert isinstance(msg, dict)    # must be dict in the correct format

        logger.info("Sending message {0}".format(msg))
        msg2 = msg.copy()
        # just to make guessing a bit harder :)
        msg2['issuedAt'] = int(time.time())
        msg2['signature'] = sign(key, secret, **msg2)
        output = StringIO.StringIO()
        with closing(DataFileWriter(output, DatumWriter(),
                                    self.schema)) as writer:
            writer.append(msg2)
            writer.flush()
            output.seek(0)
            self.socket.send(output.read())

        # Get the reply.
        reply = self.socket.recv()
        logger.info("Received reply {0}".format(reply))

    def close(self):
        self.context.destroy()


if __name__ == "__main__":
    usage = "Usage: {0} <host:port> [file]".format(sys.argv[0])

    host, port = sys.argv[1].split(':')

    client = Client(host, port)

    msg = {
        'timestamp': int(time.time()),
        'indicator': 'power'
    }
    client.send(msg, KEY, SECRET)

    msg['value'] = 5.3
    client.send(msg, KEY, SECRET)
