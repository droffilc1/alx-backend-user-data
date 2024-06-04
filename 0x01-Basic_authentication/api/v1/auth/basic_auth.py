#!/usr/bin/env python3
"""basic_auth
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Class BasicAuth that inherits from Auth
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization header for a
        Basic Authentication.
        """
        if (authorization_header is None or
                not isinstance(authorization_header, str)):
            return None

        # Check if the header starts with 'Basic '
        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header.split(' ')[1]
