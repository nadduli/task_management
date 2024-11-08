#!/usr/bin/python3
"""Error Module"""

from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse


class TaskException(Exception):
    """the base class for all task exceptions"""
    pass

class InvalidToken(TaskException):
    """user has provided an invalid token"""
    pass

class RevokedToken(TaskException):
    """user has provided a revoked token"""
    pass

class AccessTokenRequired(TaskException):
    """user has not provided an access token"""
    pass

class RefreshTokenRequired(TaskException):
    """user has not provided a refresh token"""
    pass

class UserAlreadyExists(TaskException):
    """user already exists"""
    pass

class InsufficientPermissions(TaskException):
    """user does not have the required permissions"""
    pass

class InvalidCredentials(TaskException):
    """user credentials are invalid"""
    pass

class UserNotFound(TaskException):
    """user not found"""
    pass


class TaskNotFound(TaskException):
    """task not found"""
    pass

def create_exception_handler(status_code: int, initial_detail: Any) -> Callable[[Request, Exception], JSONResponse]:
    """Create exception handler"""
    async def exception_handler(request: Request, exc: TaskException):
        return JSONResponse(
            status_code=status_code,
            content=initial_detail
        )
    return exception_handler
