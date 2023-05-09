#!/usr/bin/env python3
"""
    encrypt_password module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """encrypt user passwords using bcypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """verify is a hash matches password"""
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    return False
