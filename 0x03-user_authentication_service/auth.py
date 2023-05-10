#!/usr/bin/env python3
"""auth module"""
import bcrypt
import uuid
from db import DB, User, NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers new users"""
        try:
            if self._db.find_user_by(email=email):
                raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """validate user login"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        else:
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)

    def _generate_uuid(self):
        """returns a unique id"""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str | None:
        """returns a users session ID"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return
        else:
            id = self._generate_uuid()
            self._db.update_user(user.id, session_id=id)
            return id


def _hash_password(password: str) -> bytes:
    """return a a hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
