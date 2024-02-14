#!/usr/bin/env python3
""" Module of session authontication
"""
from flask import request
from typing import List, TypeVar
from models.user import User
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ Class SessionAuth that inherits from Auth
    """

    def __init__(self) -> None:
        """ SessionAuth constructure calls the super constructure
        """
        super().__init__()
