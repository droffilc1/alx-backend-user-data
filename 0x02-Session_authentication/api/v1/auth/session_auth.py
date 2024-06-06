#!/usr/bin/env python3
"""session_auth
Implements SessionAuth class.
"""
from uuid import uuid4
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ A class SessionAuth that inherits from Auth

    Attributes:
        - user_id_by_session_id
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        id = str(uuid4())
        self.user_id_by_session_id[id] = user_id
        return id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
