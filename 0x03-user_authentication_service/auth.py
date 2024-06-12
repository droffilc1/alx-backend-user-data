#!/usr/bin/env python3
"""auth module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ Hash password
    """
    # Convert password to bytes
    _bytes = password.encode('utf-8')

    # Generate the salt
    salt = bcrypt.gensalt()

    # Hash the password
    _hash = bcrypt.hashpw(_bytes, salt)

    # Return password hashed
    return _hash
