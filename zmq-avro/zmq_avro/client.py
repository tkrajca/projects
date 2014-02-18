#!/usr/bin/env python2

import sys
import logging
import zmq


logger = logging.getLogger('zmq_avro.client')


class Client(object):

    def send(msg):
        context = zmq.Context()

        logger.info("Connecting to hello world server…")
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")

        logger.info("Sending request %s …" % msg)
        socket.send(msg)

        # Get the reply.
        reply = socket.recv()
        logger.info("Received reply %s " % reply)


if __name__ == "__main__":
    usage = "Usage: {0} <host:port> [file]".format(sys.argv[0])

    host, port = sys.argv[1].split(':')

    client = Client(host, port)

    client.send('bla')
    client.send('blabla')
