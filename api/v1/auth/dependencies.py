#!/usr/bin/python3
"""Authentication Module"""

from fastapi import Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from .utils import decode_access_token


class AccessTokenBearer(HTTPBearer):
    """Protects endpoints by requiring a valid access token."""

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        creds = await super().__call__(request)
        token = creds.credentials

        token_data = decode_access_token(token)

        if not self.valid_token(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token"
            )
        if token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a valid access token",
            )
        return token_data

    def valid_token(self, token: str) -> bool:
        """validate token"""
        token_data = decode_access_token(token)
        return True if token_data is not None else False
