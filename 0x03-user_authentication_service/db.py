#!/usr/bin/env python3
""" DB module """
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound


from user import Base, User
from typing import List, Union


class DB:
    """ DB class
    """

    COLUMNS = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']

    def __init__(self) -> None:
        """ Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """ Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Method that saves the user to the database """
        # check the email passed and hashed password
        if not email or not hashed_password:
            return None
        # create a user obj
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        # insert it to the db
        session.add(user)
        # commit the changes
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ Method that finds and retrieves users from db """
        # find the user
        user = self._session.query(User).filter_by(**kwargs).first()
        # check the user obj
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Method that updates a user into the database of users """
        # find the user by id
        user = self.find_user_by(id=user_id)
        # check the user obj
        if not user:
            return None
        # loop over the kwargs
        for key, value in kwargs.items():
            if key not in DB.COLUMNS:
                raise ValueError
            # update the user attributes
            setattr(user, key, value)
        # commit the changes
        self._session.commit()
        return None
