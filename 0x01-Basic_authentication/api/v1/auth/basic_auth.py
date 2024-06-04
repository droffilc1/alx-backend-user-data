#!/usr/bin/env python3
"""basic_auth
"""
import base64
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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Returns the decoded value of a Base64 string
        """
        if (base64_authorization_header is None or
                not isinstance(base64_authorization_header, str)):
            return None

        try:
            decoded_string = base64.b64decode(base64_authorization_header)
            return decoded_string.decode('utf-8')
        except Exception:
            return None
