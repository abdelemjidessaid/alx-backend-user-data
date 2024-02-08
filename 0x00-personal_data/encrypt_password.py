#!/usr/bin/env python3
"""
    Module of encryption of passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
        Function that encrypts the passwords with generated salt
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
        Function that checks the encryped password and the real one
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
