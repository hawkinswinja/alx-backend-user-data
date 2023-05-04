#!/usr/bin/env python3
"""module BasicAuth"""
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
import re
import base64


class BasicAuth(Auth):
    """Module that implements basic authentication"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """verifies base64 encoding"""
        if not authorization_header:
            return None
        if type(authorization_header) != str:
            return None
        if re.search(r'^Basic ', authorization_header):
            return authorization_header.split()[1]
        else:
            return None

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """return decode value of auth"""
        if not base64_authorization_header:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            data = base64.b64decode(base64_authorization_header)
            return data.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """return current user email and password"""
        if type(decoded_base64_authorization_header) == str:
            if ':' in decoded_base64_authorization_header:
                user = decoded_base64_authorization_header.split(':')
                return (user[0], user[1])
        return (None, None)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """get a user from DB"""
        if type(user_email) == str and type(user_pwd) == str:
            user = User.search({'email': user_email})
            if len(user):
                user = user[0]
                if user.is_valid_password(user_pwd):
                    return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns data for current user"""
        autherization = self.authorization_header(request)
        token = self.extract_base64_authorization_header(autherization)
        token = self.decode_base64_authorization_header(token)
        user_data = self.extract_user_credentials(token)
        return self.user_object_from_credentials(user_email=user_data[0],
                                                 user_pwd=user_data[1])
