#!/usr/bin/env python
"""
zmq-avro
========

TODO: (v0.9)
zmq-avro

:copyright: (c) 2014 Tomas Krajca, see AUTHORS for more details.

:license: BSD-3-clause, see LICENSE for more details.
"""
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from pkg_resources import parse_version

import os

# Hack to prevent stupid "TypeError: 'NoneType' object is not callable" error
# in multiprocessing/util.py _exit_function when running `python
# setup.py test` (see
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
for m in ('multiprocessing', 'billiard'):
    try:
        __import__(m)
    except ImportError:
        pass


tests_require = [
]


install_requires = [
    'PyZMQ',
    'avro',
]

version = __import__('zmq_avro').get_version()

setup(
    name='zmq-avro',
    version=version,
    author='Tomas Krajca',
    author_email=('t.l.krajca@gmail.com',),
    url='https://github.com/tkrajca/projects/zmq-avro/',
    description=('TODO'),
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite='tests',
    license='BSD-3-Clause',
    scripts=['zmq_avro/client.py', 'zmq_avro/server.py'],
    include_package_data=True,
    keywords="TODO",
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD-3-Clause',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
    ],
)
