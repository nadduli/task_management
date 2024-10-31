#!/usr/bin/python3
"""Authentication Module"""

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


class AccessTokenBearer(HTTPBearer):
    """protect endpoints from """
    pass