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
        Returns: True if path is None
                 True if excluded_paths is None or empty
                 False if path is in excluded_paths
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Normalize paths by stripping trailing slashes
        path = path.rstrip('/')
        excluded_paths = [p.rstrip('/') for p in excluded_paths]

        for excluded_path in excluded_paths:
            # Handle wildcard: remove the '*' and check if path starts
            # with excluded_path
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        return True

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
