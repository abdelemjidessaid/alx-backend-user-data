#!/usr/bin/env python3
""" Module of authentication
"""
from flask import request
from typing import List, TypeVar
import os
import re
from models.user import User


class Auth:
    """ Class of authentication
    """

    def __init__(self) -> None:
        """ Class constructure
        """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method that checks if a path requires authentication.
        """
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Method that check the authorization of headers
        """
        if request:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """ Method that returns the user
        """
        return None

    def session_cookie(self, request=None):
        """ Method that returns a cookie value from request
        """
        if not request:
            return None
        return request.cookies.get(os.environ.get('SESSION_NAME'))
