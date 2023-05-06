#!/usr/bin/env python3
"""module class for session authentication"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import uuid
from os import getenv
from flask import request, jsonify, abort
from api.v1.views import sa_views


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

    def current_user(self, request=None) -> TypeVar('User'):
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


@sa_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """login form for session authentication"""
    email = request.form.get('email')
    pwd = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not pwd:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(pwd):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    auth.create_session(user[0].id)
    response = jsonify(user[0].to_json())
    response.set_cookie(getenv('SESSION_NAME'), user[0].id)
    return response


@sa_views.route('/api/v1/auth_session/logout', methods=['DELETE'],
                strict_slashes=False)
def destroy_session():
    """logout user"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
