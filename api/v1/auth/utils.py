#!/usr/bin/python3
"""Password Hashing Module"""

from passlib.context import CryptContext


password_context = CryptContext(schemes=["bcrypt"])


def generate_password_hash(password: str) -> str:
    """Generate password hash"""
    hashed_password = password_context.hash(password)
    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password function"""
    return password_context.verify(password, hashed_password)
