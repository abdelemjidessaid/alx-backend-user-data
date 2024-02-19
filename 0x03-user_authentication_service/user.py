#!/usr/bin/env python3
""" Module of User Model """
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column


Base = declarative_base()


class User(Base):
    """ Class of User """

    # the table name
    __tablename__ = 'users'
    # the table columns initialization
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
