# usr/bin/env python3
"""encrypt_password."""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password."""
    # Convert the password to bytes
    password_bytes = password.encode('utf-8')

    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password
