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
