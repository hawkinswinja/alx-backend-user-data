#!/usr/bin/env python3
"""this module defines the class Auth"""
from flask import request
from typing import List, TypeVar


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
