#!/usr/bin/python3
"""Password Hashing Module"""

from datetime import timedelta, datetime
from passlib.context import CryptContext
import jwt
import uuid
import logging
from api.core.config import Config


password_context = CryptContext(schemes=["bcrypt"])

ACCESS_TOKEN_EXPIRY = 3600


def generate_password_hash(password: str) -> str:
    """Generate password hash"""
    hashed_password = password_context.hash(password)
    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password function"""
    return password_context.verify(password, hashed_password)


def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    """Create JWT access token"""

    payload = {
        "user": user_data,
        "jti": str(uuid.uuid4()),
        "exp": datetime.now()
        + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)),
        refresh: refresh

    }

    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM
    )

    return token

def decode_access_token(token: str):
    """Decode a jwt access token"""
    try:
        token_data = jwt.decode(
            jwt = token,
            key=Config.JWT_SECRET,
            algorithm=Config.JWT_ALGORITHM
            )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None