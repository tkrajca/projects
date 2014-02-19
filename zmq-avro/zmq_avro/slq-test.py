from sqlalchemy import (create_engine, Column, Integer, String, DateTime,
                        ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import datetime

db = create_engine('sqlite://')     # in memory

#db.echo = False

# table definitions
Base = declarative_base()


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

Base.metadata.create_all(db)
# END table definitions

Session = sessionmaker(bind=db)
session = Session()

# insert data
user = User(key='abcdefg', secret='abcdefg01234567890')
session.add(user)
session.commit()
# END insert data

for user in session.query(User).filter_by(key='abcdefg'):
    print(user.id, user.key)
