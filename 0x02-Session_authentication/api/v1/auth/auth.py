#!/usr/bin/env python3
"""this module defines the class Auth"""
from typing import List, TypeVar
from os import getenv


class Auth():
    """Session and user authentication module"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """checks if path requires authentication"""
        if not path:
            return True
        if not excluded_paths or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns the authorization value"""
        if request is None:
            return None
        if 'Authorization' in request.headers:
            return request.headers.get('Authorization')
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None"""
        return None

    def session_cookie(self, request=None):
        """return a cookie value from a request"""
        if not request:
            return
        return request.cookies.get(getenv('SESSION_NAME'))
