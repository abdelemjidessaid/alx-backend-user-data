#!/usr/bin/env python3
""" Module of authentication
"""
from flask import request
from typing import List, TypeVar
from models.user import User


class Auth:
    """ Class of authentication
    """

    def __init__(self) -> None:
        """ Class constructure
        """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method that require the authentication
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Method that check the authorizations
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """ Method that returns the user
        """
        return None
