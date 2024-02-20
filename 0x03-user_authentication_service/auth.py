#!/usr/bin/env python3
""" Module of authentication """
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """ Function that hashes the passwords """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def _generate_uuid() -> str:
    """ Method that generates new UUID """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Method that registers user and return it """
        if not email or not password:
            return None

        hashed_password = _hash_password(password=password)
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user:
            raise ValueError(f'User {user.email} already exists.')
        return self._db.add_user(email=email, hashed_password=hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """ Method that validates login info """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        if user:
            return bcrypt.checkpw(
                password=password.encode('utf-8'),
                hashed_password=user.hashed_password)
        return False
