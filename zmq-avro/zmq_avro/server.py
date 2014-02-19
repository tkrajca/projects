#!/usr/bin/env python2

import sys
import logging
import zmq
import threading
import StringIO

from avro.datafile import DataFileReader
from avro.io import DatumReader

from contextlib import closing

from zmq_avro import models
from zmq_avro import utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('zmq_avro.server')


class Server(threading.Thread):
    _last_msg = None
    terminate = False

    def __init__(self, host, port, *args, **kwargs):
        self.host = host
        self.port = port
        self.db, self.Session = models.init_db()
        # load a testing user
        # TODO: remove before production :)
        with closing(self.Session()) as session:
            user = models.User(key=models.KEY, secret=models.SECRET)
            session.add(user)
            session.commit()
        super(Server, self).__init__(*args, **kwargs)

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        logger.info("Binding to {0}:{1}".format(self.host, self.port))
        socket.bind("tcp://{0}:{1}".format(self.host, self.port))

        session = self.Session()

        while True:
            if self.terminate:
                break

            # Wait for next request from client
            try:
                self._last_msg = socket.recv(zmq.NOBLOCK)
            except zmq.ZMQError:
                continue

            input = StringIO.StringIO()
            input.write(self._last_msg)
            input.seek(0)
            with closing(DataFileReader(input, DatumReader())) as reader:
                for data in reader:
                    logger.info("Received message {0}".format(data))
                    user = utils.verify(session, data)
                    if user:
                        logger.info("The received message is valid.")
                        socket.send(b"OK")
                        audit = models.Audit(
                            user=user.id, action='Received a valid message.')
                        session.add(audit)
                        session.commit()
                    else:
                        logger.warning("The received message is invalid.")
                        socket.send(b"INVALID!")

        context.destroy()
        logger.info("Dumping out contents of the Audit table:")
        for audit in session.query(models.Audit).order_by(
                models.Audit.timestamp):
            logger.info("{0}\t{1}:{2}".format(audit.timestamp, audit.user,
                                              audit.action))
        session.close()

    def close(self):
        self.terminate = True


if __name__ == "__main__":
    usage = "Usage: {0} <host:port>".format(sys.argv[0])

    host, port = sys.argv[1].split(':')

    server = Server(host, port)
    server.run()
