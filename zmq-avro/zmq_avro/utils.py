import hashlib

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from zmq_avro import models


def sign(key, secret, *args, **kwargs):
    msg2 = kwargs.copy()
    if 'signature' in msg2:
        del msg2['signature']
    if 'value' in msg2:
        del msg2['value']
    msg = ".".join(args)
    msg += ".".join("{0}={1}".format(key, value) for key, value in
                    msg2.iteritems())
    return "{0}:{1}".format(key, hashlib.md5(secret + msg).hexdigest())


def verify(session, msg):
    key, _ = msg['signature'].split(':')
    try:
        user = session.query(models.User).filter_by(key=key).one()
    except (NoResultFound, MultipleResultsFound):
        return None

    return (msg['signature'] == sign(user.key, user.secret, **msg) and
            user or None)
