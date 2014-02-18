#!/usr/bin/env python2

import sys
import logging
import zmq
import threading


logger = logging.getLogger('zmq_avro.server')


class Server(threading.Thread):
    _last_msg = None
    terminate = False

    def __init__(self, host, port, *args, **kwargs):
        self.host = host
        self.port = port
        self.context = zmq.Context()
        super(Server, self).__init__(*args, **kwargs)

    def run(self):
        socket = self.context.socket(zmq.REP)
        socket.bind("tcp://{0}:{1}".format(self.host, self.port))

        # will probably need to threading or multiprocessing here
        while True:
            # Wait for next request from client
            if self.terminate:
                break

            try:
                self._last_msg = socket.recv(zmq.NOBLOCK)
            except zmq.ZMQError:
                continue

            print("Received request: %s" % self._last_msg)
            logger.info("Received request: %s" % self._last_msg)

            # Send reply back to client
            socket.send(b"OK")

        self.context.destroy()

    def close(self):
        self.terminate = True


if __name__ == "__main__":
    usage = "Usage: {0} <host:port>".format(sys.argv[0])

    host, port = sys.argv[1].split(':')

    server = Server(host, port)
    server.run()
