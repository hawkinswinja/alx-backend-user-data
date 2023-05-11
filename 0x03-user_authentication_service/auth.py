#!/usr/bin/env python3
"""auth module"""
import bcrypt
import uuid
# from typing import Union
from db import DB, User, NoResultFound


def _hash_password(password: str) -> bytes:
    """return a hashed password"""
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash


def _generate_uuid() -> str:
    """returns a unique id"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers new users"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """validate user login"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str | None:
        """returns a users session ID"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        id = _generate_uuid()
        self._db.update_user(user.id, session_id=id)
        return id
