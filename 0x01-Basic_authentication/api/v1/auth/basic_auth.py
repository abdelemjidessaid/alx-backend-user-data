#!/usr/bin/env python3
""" Module of basic authentication
"""
from flask import request
from typing import List, TypeVar
import base64
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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Function that decodes the Base64
        """
        if not base64_authorization_header:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            result = base64.decodebytes(
                base64_authorization_header.encode('utf-8')
            )
            return result.decode('utf-8')
            
        except:
            return None
