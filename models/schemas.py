from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    keys = relationship('Key', secondary='key_users', back_populates='users')


class Key(Base):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True)
    value = Column(String)
    users = relationship('User', secondary='key_users', back_populates='keys')


class KeyUser(Base):
    __tablename__ = "key_users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    key_id = Column(Integer, ForeignKey('keys.id'))