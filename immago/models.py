from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Thread(Base):
    __tablename__ = 'thread'
    id = Column(Integer, primary_key=True)
    posts = relationship('Post', backref='thread')
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now)

    def __init__(self, created, updated):
        self.created = created
        self.updated = updated


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    thread_id = Column(Integer, ForeignKey('thread.id'), nullable=False)
    created = Column(DateTime, default=datetime.now)
    msg = Column(Text)

    def __init__(self, thread_id, created, msg):
        self.thread_id = thread_id
        self.created = created
        self.msg = msg
