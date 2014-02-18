#!/usr/bin/env python2

import sys
import logging
import zmq


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
        # TODO: close this connection at the end

    def send(self, msg):
        print("Sending message %s " % msg)
        logger.info("Sending message %s " % msg)
        self.socket.send(msg)

        # Get the reply.
        reply = self.socket.recv()
        print("Received reply %s " % reply)
        logger.info("Received reply %s " % reply)

    def close(self):
        self.context.destroy()


if __name__ == "__main__":
    usage = "Usage: {0} <host:port> [file]".format(sys.argv[0])

    host, port = sys.argv[1].split(':')

    client = Client(host, port)

    client.send('bla')
    client.send('blabla')
