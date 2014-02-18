#!/usr/bin/env python2

import sys
import logging
import zmq

logger = logging.getLogger('zmq_avro.server')


class Server(object):
    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5555")

        while True:
            # Wait for next request from client
            msg = socket.recv()
            logger.info("Received request: %s" % msg)

            # Send reply back to client
            socket.send(b"OK")


if __name__ == "__main__":
    usage = "Usage: {0} <host:port>".format(sys.argv[0])

    host, port = sys.argv[1].split(':')

    server = Server(host, port)
    server.run()
