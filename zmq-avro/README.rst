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
`sqlite3` database and prints the original `json` data out (given the message
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

How to install
--------------

TODO
