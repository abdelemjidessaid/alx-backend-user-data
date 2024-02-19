#!/usr/bin/env python3
""" Module of SQLAchemy. Creating table of Users
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column


Base = declarative_base()


class User(Base):
    """ Class of User """

    # the table name
    __tablename__ = 'users'
    # the table columns initialization
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=False)
    reset_token = Column(String(250), nullable=False)
