#!/usr/bin/env python3
""" Module of Session expiration authentication
"""
from os import environ
from datetime import datetime
from flask import request, abort
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Class of Session Expiration Authentication
    """

    def __init__(self) -> None:
        """ SessionExpAuth constructure
        """
        super().__init__()
        try:
            duration = int(environ.get('SESSION_DURATION'))
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """ Method that creates new session by
            calling the super.create_session
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Method that calls the super.user_id_for_session_id
        """
        if not session_id:
            return None
        session = self.user_id_by_session_id.get(session_id)
        if not session:
            return None
        if self.session_duration <= 0:
            return session.get('user_id')
        created_at = session.get('created_at')
        if not created_at:
            return None
        now = datetime.now()
        if (created_at + self.session_duration) < now:
            return None
        return session.get('user_id')
