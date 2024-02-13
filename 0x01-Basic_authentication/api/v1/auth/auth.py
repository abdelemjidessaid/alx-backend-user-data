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
        if not path or not excluded_paths or len(excluded_paths) == 0:
            return True
        if path[-1] == '/':
            tmp = path[:-1]
            if tmp in excluded_paths:
                return False
        else:
            tmp = path + '/'
            if tmp in excluded_paths:
                return False
        return not(path in excluded_paths)

    def authorization_header(self, request=None) -> str:
        """ Method that check the authorization of headers
        """
        if request:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """ Method that returns the user
        """
        return None
