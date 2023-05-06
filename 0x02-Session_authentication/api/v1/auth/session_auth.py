#!/usr/bin/env python3
"""module class for session authentication"""
from .auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """Session authentication module"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID using user_id"""
        if not user_id or type(user_id) != str:
            return
        id = str(uuid.uuid4())
        self.user_id_by_session_id[id] = user_id
        return id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """retrieve user_id based on session_id"""
        if not session_id or type(session_id) != str:
            return
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """return the current authenticated user"""
        session = self.session_cookie(request)
        return User.get(self.user_id_for_session_id(session))

    def destroy_session(self, request=None):
        """remove current user session"""
        if request is None:
            return False
        session = self.session_cookie(request)
        if session and self.user_id_for_session_id(session):
            del self.user_id_by_session_id[session]
            return True
        return False
