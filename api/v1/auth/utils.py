#!/usr/bin/python3
"""Password Hashing Module"""

from datetime import timedelta, datetime
import uuid
import logging
from passlib.context import CryptContext
import jwt
from api.core.config import Config
from itsdangerous import URLSafeTimedSerializer


password_context = CryptContext(schemes=["bcrypt"])

ACCESS_TOKEN_EXPIRY = 3600


def generate_password_hash(password: str) -> str:
    """Generate password hash"""
    hashed_password = password_context.hash(password)
    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password function"""
    return password_context.verify(password, hashed_password)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    """Create JWT access token"""
    payload = {}

    payload["user"] = user_data
    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )

    payload["jti"] = str(uuid.uuid4())

    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM
    )
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return token


def decode_access_token(token: str) -> dict:
    """Decode a jwt access token"""
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM]
        )

        return token_data

    except jwt.PyJWTError as e:
        logging.exception(e)
        return None


salt = "email-configuration"

serializer = URLSafeTimedSerializer(secret_key=Config.JWT_SECRET, salt=salt)


def create_url_safe_token(data: dict):
    """Create url safe token"""
    token = serializer.dumps(data, salt=salt)
    return token


def decode_url_safe_token(token: str):
    """Decode url safe token"""
    try:
        data = serializer.loads(token, salt=salt)
        return data
    except Exception as e:
        logging.error(str(e))

def generate_magic_link_token(email: str) -> str:
    """Generate magic link token"""
    salt = "magic-link"
    return serializer.dumps({"email": email}, salt=salt)

def verify_magic_link_token(token: str):
    """Verify magic link token"""
    salt = "magic-link"
    try:
        email = serializer.loads(token, salt=salt, max_age=3600)
        return email
    except Exception as e:
        logging.error(str(e))
