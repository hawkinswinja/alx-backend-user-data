#!/usr/bin/env python3
"""auth module"""
import bcrypt
import uuid
from typing import Union
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
        except Exception:
            return False
        return bcrypt.checkpw(password.encode('utf-8'),
                              user.hashed_password)

    def create_session(self, email: str) -> Union[str, None]:
        """returns a users session ID"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        id = _generate_uuid()
        self._db.update_user(user.id, session_id=id)
        return id

    def get_user_from_session_id(self, session_id: str) -> User | None:
        """get user based on session id"""
        if session_id:
            try:
                return self._db.find_user_by(session_id=session_id)
            except Exception:
                pass
        return None

    def destroy_session(self, user_id: int) -> None:
        """remove user's session_id"""
        if user_id:
            self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """retrieves user reset password"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_id = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_id)
        return reset_id

    def update_password(self, reset_token: str, password: str) -> None:
        """update user password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)
