#!/usr/bin/python3
"""Error Module"""

from fastapi import HTTPException, status


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

class InternalServerError(TaskException):
    """internal server error"""
    pass

class TaskNotFound(TaskException):
    """task not found"""
    pass



