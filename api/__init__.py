#!/usr/bin/python3
"""
Main entry point of the Task Management application.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, status, HTTPException
from api.v1.tasks.routes import task_router
from api.v1.auth.routes import auth_router
from fastapi.responses import JSONResponse

from api.db.database import init_db
from api.v1.errors import (
    TaskNotFound,
    UserAlreadyExists,
    UserNotFound,
    InvalidCredentials,
    InvalidToken,
    RevokedToken,
    RefreshTokenRequired,
    AccessTokenRequired,
    InsufficientPermissions,
    InvalidCredentials,
    create_exception_handler
)


@asynccontextmanager
async def life_span(app: FastAPI):
    """method to run when starting the app"""
    print("Connected to the database..!")
    await init_db()
    yield
    print("Disconnected from the database...!")


VERSION = "v1"

app = FastAPI(
    title="Tasks Management API",
    description="**Advanced Task Management API**",
    version=VERSION,
    #lifespan=life_span,
    terms_of_service="http://danielInnovations.com/terms/",
    contact={
        "name": "API Support",
        "url": "http://danielInnovations.com/support",
        "email": "naddulidaniel1994@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.add_exception_handler(
    UserAlreadyExists,
    create_exception_handler(
        status_code=status.HTTP_409_CONFLICT,
        initial_detail={
            "message": "User with email already exists",
            "error_code": "USER_ALREADY_EXISTS"
        }
        )
)
app.add_exception_handler(
    UserNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "User not found",
            "error_code": "USER_NOT_FOUND"
        }
        )
)
app.add_exception_handler(
    InvalidCredentials,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Invalid credentials",
            "error_code": "INVALID_CREDENTIALS"
        }
        )
)
app.add_exception_handler(
    InvalidToken,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Invalid token",
            "error_code": "INVALID_TOKEN"
        }
        )  
)
app.add_exception_handler(
    RevokedToken,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Token has been revoked",
            "error_code": "REVOKED_TOKEN"
        }
        )
)
app.add_exception_handler(
    RefreshTokenRequired,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Refresh token is required",
            "error_code": "REFRESH_TOKEN_REQUIRED"
        }
        )
)
app.add_exception_handler(
    AccessTokenRequired,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Access token is required",
            "error_code": "ACCESS_TOKEN_REQUIRED"
        }
        )
)
app.add_exception_handler(
    InsufficientPermissions,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "Insufficient permissions",
            "error_code": "INSUFFICIENT_PERMISSIONS"
        }
        )
)

app.add_exception_handler(
    TaskNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "Task not found",
            "error_code": "TASK_NOT_FOUND"
        }
        )
)

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Internal server error",
            "error_code": "INTERNAL_SERVER_ERROR"
        }
    )

app.include_router(auth_router, prefix=f"/api/{VERSION}/auth", tags=["auth"])
app.include_router(task_router, prefix=f"/api/{VERSION}/tasks", tags=["tasks"])
