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

    def create_session(self, email: str) -> str:
        """ Method that creates a session
            Return:
                Session ID
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Method that returns the user by its session id
            Return:
                User by its Session ID
        """
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                return None
        return None

    def destroy_session(self, user_id: int) -> None:
        """ Method that delets the user session id """
        self._db.update_user(user_id=user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ Method that resets the user password token """
        try:
            user = self._db.find_user_by(email=email)
            if not user:
                raise ValueError
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ Method that updates the user password
            Args:
                - reset_token: the token of reset password
                - password: the new passwords that should be applied
            Return:
                - None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed = _hash_password(password=password)
            self._db.update_user(
                user.id, hashed_password=hashed,
                reset_token=None)
        except NoResultFound:
            raise ValueError
