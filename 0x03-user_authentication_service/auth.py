#!/usr/bin/env python3
""" Module of authentication """
import bcrypt


def _hash_password(password: str) -> bytes:
    """ Function that hashes the passwords """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed
