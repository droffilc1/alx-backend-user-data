# usr/bin/env python3
"""encrypt_password."""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password."""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'),
                                    bcrypt.gensalt())
    return hashed_password
