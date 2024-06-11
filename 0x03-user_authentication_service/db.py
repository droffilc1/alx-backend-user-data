#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Adds a user to the database
        Returns a User object
        """
        # Create session
        session = self._session

        # Add User object
        new_user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(new_user)
            self._session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Returns first row found in the users table as filtered
        by the method's input arguments.
        """
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except (NoResultFound, InvalidRequestError) as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates user
        """
        session = self._session
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if hasattr(User, key):
                    setattr(user, key, value)
                else:
                    raise ValueError
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
