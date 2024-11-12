#!/usr/bin/python3
"""Error Module"""

from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError


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


class AccountNotVerified(TaskException):
    """account not verified"""

    pass


class PasswordsDoNotMatch(TaskException):
    """passwords do not match"""

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
                "resolution": "Please use a different email",
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
                "resolution": "Please check your credentials and try again",
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
                "resolution": "Please check your credentials and try again",
            },
        ),
    )
    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Invalid token",
                "error_code": "INVALID_TOKEN",
                "resolution": "Please log in again",
            },
        ),
    )
    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token has been revoked",
                "error_code": "REVOKED_TOKEN",
                "resolution": "Please log in again",
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
                "resolution": "Please log in to get a refresh token",
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
                "resolution": "Please log in to get an access token",
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
                "resolution": "Please check your permissions and try again",
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
                "resolution": "Please check the task ID and try again",
            },
        ),
    )

    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Account not verified",
                "error_code": "ACCOUNT_NOT_VERIFIED",
                "resolution": "Please check your email to verify your account",
            },
        ),
    )

    app.add_exception_handler(
        PasswordsDoNotMatch,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Passwords do not match",
                "error_code": "PASSWORDS_DO_NOT_MATCH",
                "resolution": "Please check your passwords and try again",
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
                "resolution": "Please try again later",
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def database__error(request, exc):
        print(str(exc))
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
                "resolution": "Please try again later",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
