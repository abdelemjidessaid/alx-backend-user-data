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
