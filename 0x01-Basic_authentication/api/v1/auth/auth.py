#!/usr/bin/env python3
"""
Template for authentication system
"""
from typing import List, TypeVar
from flask import request
from models.user import User


class Auth:
    """
    Class Auth
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Defines public method `require_auth`
        Args:
          - path
          - excluded_paths
        Returns: False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Defines public method `authorization_header`
        Args:
          -request: Flask object
        Returns: None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Defines public method `current_user`
        Args:
          -request: Flask object
        Returns: None
        """
        return None
