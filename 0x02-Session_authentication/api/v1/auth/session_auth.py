#!/usr/bin/env python3
""" Module of session authontication
"""
from flask import request
from typing import List, TypeVar
from uuid import uuid4
from models.user import User
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ Class SessionAuth that inherits from Auth
    """
    user_id_by_session_id = {}

    def __init__(self) -> None:
        """ SessionAuth constructure calls the super constructure
        """
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """ Function that creates new session
        """
        if not user_id or not isinstance(user_id, str):
            return None
        id = str(uuid4())
        SessionAuth.user_id_by_session_id[id] = user_id
        return id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Method that returns the User ID based on session_id
        """
        if not session_id or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """ Method that returns a User instance based on the cookie value
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ Method that deletes the user session -> logout
        """
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id or user_id == '':
            return False
        del self.user_id_by_session_id[session_id]
        return True
