#!/usr/bin/python3
"""Error Module"""

from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status


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


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    """Create exception handler"""

    async def exception_handler(request: Request, exc: TaskException):
        return JSONResponse(status_code=status_code, content=initial_detail)

    return exception_handler


def register_all_errors(app: FastAPI):
    """Register all errors"""
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={
                "message": "User with email already exists",
                "error_code": "USER_ALREADY_EXISTS",
            },
        ),
    )
    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "User not found",
                "error_code": "USER_NOT_FOUND",
            },
        ),
    )
    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Invalid credentials",
                "error_code": "INVALID_CREDENTIALS",
            },
        ),
    )
    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={"message": "Invalid token", "error_code": "INVALID_TOKEN"},
        ),
    )
    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token has been revoked",
                "error_code": "REVOKED_TOKEN",
            },
        ),
    )
    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Refresh token is required",
                "error_code": "REFRESH_TOKEN_REQUIRED",
            },
        ),
    )
    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Access token is required",
                "error_code": "ACCESS_TOKEN_REQUIRED",
            },
        ),
    )
    app.add_exception_handler(
        InsufficientPermissions,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Insufficient permissions",
                "error_code": "INSUFFICIENT_PERMISSIONS",
            },
        ),
    )

    app.add_exception_handler(
        TaskNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Task not found",
                "error_code": "TASK_NOT_FOUND",
            },
        ),
    )

    @app.exception_handler(500)
    async def internal_error_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Internal server error",
                "error_code": "INTERNAL_SERVER_ERROR",
            },
        )
