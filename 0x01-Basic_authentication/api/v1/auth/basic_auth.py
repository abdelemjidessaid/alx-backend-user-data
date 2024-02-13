#!/usr/bin/env python3
""" Module of basic authentication
"""
from flask import request
from typing import List, TypeVar
from models.user import User
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Class of Basic Authentication
    """

    def __init__(self) -> None:
        """ Class constructure
        """
        super().__init__()

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Function that generates and returns a Base64 Authorization
        """
        if not authorization_header:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        else:
            return authorization_header.split(' ')[1]
