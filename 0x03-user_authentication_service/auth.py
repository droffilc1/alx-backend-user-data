#!/usr/bin/env python3
"""auth module
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
import uuid
from db import DB
from user import User


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


def _generate_uuid() -> str:
    """Generates UUIDs
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize a new Auth instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a user
        """
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        # Hash password
        hashed = _hash_password(password)

        # Add a new user to the database
        new_user = self._db.add_user(email, hashed)
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates credentials
        """
        try:
            user = self._db.find_user_by(email=email)
            pw_encode = password.encode('utf-8')
            return bcrypt.checkpw(pw_encode, user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Get session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            return user.session_id
        except NoResultFound:
            return None
