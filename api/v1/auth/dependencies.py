#!/usr/bin/python3
"""Authentication Module"""

from fastapi import Request, status, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import decode_access_token
from api.db.redis import token_in_blocklist
from api.db.database import get_session
from .service import UserService


user_service = UserService()

class TokenBearer(HTTPBearer):
    """Protects endpoints by requiring a valid access token."""

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        creds = await super().__call__(request)

        if not creds or not creds.credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing",
            )
        token = creds.credentials

        token_data = decode_access_token(token)

        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token"
            )

        if not self.valid_token(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail={
                    "error": "This token is invalid or has been revoked",
                    "resolution": "Please get a new token"
                }
            )
        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail={
                    "error": "This token is invalid or has been revoked",
                    "resolution": "Please get a new token"
                }
            )
        self.verify_token_data(token_data)

        return token_data

    def valid_token(self, token: str) -> bool:
        """validate token"""
        token_data = decode_access_token(token)
        return token_data is not None

    def verify_token_data(self, token_data):
        """override this method in child classes"""
        raise NotImplementedError(
            "Please Override this method in child classes")


class AccessTokenBearer(TokenBearer):
    """Protects endpoints by requiring a valid access token."""

    def verify_token_data(self, token_data: dict) -> None:
        """verify access_token data"""
        if token_data and token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a valid access token",
            )


class RefreshTokenBearer(TokenBearer):
    """Protects endpoints by requiring a valid refresh token."""

    def verify_token_data(self, token_data: dict) -> None:
        """Verify refresh token data."""
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a valid refresh token",
            )

async def get_current_user(token_details: dict = Depends(AccessTokenBearer()),
                     session: AsyncSession = Depends(get_session)):
    """Get current logged in user details"""
    user_email = token_details['user']['email']
    user = await user_service.get_user(user_email, session)
    return user




