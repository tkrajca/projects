ZMQ-AVRO
========

This is a small project that demonstrates communcation of `Avro`_-serialized
json data over a `ZeroMQ`_ channel.

.. _Avro: http://avro.apache.org/
.. _ZeroMQ: http://zeromq.org/

Overview
--------

The project utilizes a client-server architecture.

The client reads `json` data, serializes it into `avro` and sends it over
`ZeroMQ` to the server.

The server reads `avro`-serialized data from ZeroMQ, logs the action into
`sqlite3` database and logs the original `json` data (given the message
passes authentication test).

The authentication is based on the `Amazon's S3 authentication`_ scheme. The
client has an API key and an API secret, the server has a database of API keys
and API secrets. The client concatenates certain parts of the original json
message and signs/encrypts it with its API secret. The client appends its API
key and a "signature" of the message into the original json. The server than
verifies if the data was signed with a correct API secret (for the given API
key).

There is one test case that tests the above story.

.. _Amazon's S3 authentication: http://docs.aws.amazon.com/AmazonS3/latest/dev/RESTAuthentication.html

Requirements
------------
- Tested on Python 2.7
- ZeroMQ
- Avro
- SqlAlchemy

Installation
------------

1. To develop::

    $ git clone https://github.com/tkrajca/projects/
    $ cd projects/zmq-avro
    $ python setup.py develop

2. Standalone install::

    $ git clone https://github.com/tkrajca/projects/
    $ cd projects/zmq-avro
    $ python setup.py install

Usage
-----

1. Ipython shell
    
   server::

        In [1]: from zmq_avro.server import Server

        In [2]: server = Server('127.0.0.1', '12345')
        In [3]: server.run()

   client::

        In [1]: from zmq_avro.client import Client
        In [2]: from zmq_avro import models
        In [3]: import time

        In [4]: client = Client('127.0.0.1', '12345')
        In [5]: message = {'indicator': 'power', 'timestamp': int(time.time())}
        In [6]: client.send(message, models.KEY, models.SECRET)

        In [7]: message = {'name': 'Another name', 'email': 'another@example.com'}
        In [8]: client.send(json.dumps(message), key, secret)

2. Linux shell::

    $ server.py 127.0.0.1:12345

   and::

    $ client.py 127.0.0.1:12345


Tests
-----

::

    $ python setup.py test

TODO
----

Make the client read from stdin:::

    $ client.py 127.0.0.1:12345 < example.json
