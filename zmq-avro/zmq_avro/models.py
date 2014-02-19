from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey,
                        create_engine)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import datetime

Base = declarative_base()

KEY = 'tomas'
SECRET = 'Password12345'


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    key = Column(String(64), unique=True, index=True)
    secret = Column(String(64))


class Audit(Base):
    __tablename__ = 'audit'

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('user.id'), index=True)
    action = Column(String(64))
    timestamp = Column(DateTime, default=datetime.datetime.now)


def init_db():
    # TODO: should probably make sure the database is only initialized once
    db = create_engine('sqlite://')     # in memory
    Base.metadata.create_all(db)
    Session = sessionmaker(bind=db)
    return db, Session
