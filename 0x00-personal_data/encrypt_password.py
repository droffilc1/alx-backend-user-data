#!/usr/bin/env python3
"""encrypt_password."""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password."""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'),
                                    bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates that the provided password matches the hashed password"""

    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
